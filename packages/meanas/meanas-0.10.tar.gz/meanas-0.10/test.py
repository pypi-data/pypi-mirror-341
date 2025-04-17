from typing import Tuple
import multiprocessing
import logging
import copy
from itertools import chain

import pyopencl, meanas, gridlock
import numpy
from numpy import pi, sin, cos, exp
from numpy.linalg import norm

from meanas import fdtd, fdfd
from meanas.fdmath import vec
from meanas.fdfd.waveguide_3d import compute_source, compute_overlap_e
from meanas.fdfd import operators
from meanas.fdtd import maxwell_e, maxwell_h, cpml_params, updates_with_cpml, poynting


numpy.set_printoptions(linewidth=int(1e10))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('pyopencl').setLevel(logging.WARNING)
logging.getLogger('pytools').setLevel(logging.WARNING)


fh = logging.FileHandler('opt.log')
fh.setLevel(logging.INFO)
logger.addHandler(fh)


def saveplot_2d_mp(*args):
    multiprocessing.Process(target=saveplot_2d, args=args).start()


def saveplot_2d(val, name, xz_coords):
    val = numpy.squeeze(val)
    pyplot.figure(figsize=(8, 6))
    xz_grids = numpy.meshgrid(*xz_coords, indexing='ij')
    vmax = numpy.abs(val).max()
    if (val < 0).any():
        args = {'vmin': -vmax, 'vmax': vmax, 'cmap': 'seismic'}
    else:
        args = {'vmin': 0, 'vmax': vmax, 'cmap': 'hot'}

    pyplot.pcolormesh(*xz_grids, val, **args)
    pyplot.colorbar(orientation='horizontal')
    pyplot.title(f'{name}')
    pyplot.gca().set_aspect('equal', adjustable='box')
    pyplot.savefig(f'{name}.png', dpi=240)
    pyplot.close()


def pulse(wl, dwl, dt, turn_on=1e-10):
    # dt * dw = 4 * ln(2)
    w = 2 * pi / wl
    freq = 1 / wl
    fwhm = dwl * w * w / (2 * pi)
    alpha = (fwhm * fwhm) / 8 * numpy.log(2)
    delay = numpy.sqrt(-numpy.log(turn_on) / alpha)
    delay = numpy.ceil(delay * freq) / freq     # force delay to integer number of periods to maintain phase
    logger.info(f'src_time {2 * delay / dt}')

    n = numpy.floor(pi / (w * dt))
    logger.info(f'save timestep would be {n} * dt = {n * dt}')

    # nrm = numpy.exp(-w * w / alpha) / 2

    def source_phasor(i):
        t0 = i * dt - delay
        envelope = numpy.sqrt(numpy.sqrt(2 * alpha / pi)) * numpy.exp(-alpha * t0**2)
        # if t0 < 0:
        #    envelope = numpy.exp(-alpha * t0**2)
        # else:
        #    envelope = 1
        return envelope, numpy.cos(w * t0), numpy.sin(w * t0)
    return source_phasor, delay, n #, nrm


def get_wgmode_xp(half_dims, polarity, grid, epsilon, wl, dxes):
    dims = [-half_dims, half_dims]
    dims[0][0] = dims[1][0]
    ind_dims = (grid.pos2ind(dims[0], which_shifts=None).astype(int),
                grid.pos2ind(dims[1], which_shifts=None).astype(int))
    wg_slices = tuple(slice(i, f+1) for i, f in zip(*ind_dims))
    wg_args = {
        'omega': 2 * pi / wl,
        'slices': wg_slices,
        'dxes': dxes,
        'axis': 0,
        'polarity': polarity,
        }

    wg_results = fdfd.waveguide_3d.solve_mode(mode_number=0, **wg_args, epsilon=epsilon)
    return wg_args, wg_results


def get_gaussian(m, grid, dxes, wl):
    def grid2gaussian(xyz, center, w0=4600, tilt=numpy.deg2rad(-8)):
        xs, ys, zs = xyz
        xs -= center[0]
        ys -= center[1]
        zs -= center[2]
        xg, yg, zg = numpy.meshgrid(xs, ys, zs, indexing='ij')

        rot = numpy.array([[ cos(tilt), 0, sin(tilt)],
                           [         0, 1,         0],
                           [-sin(tilt), 0, cos(tilt)]])

        x, y, z = (rot @ numpy.stack((xg.ravel(), yg.ravel(), zg.ravel()))).reshape(3, *grid.shape)
        r2 = x * x + y * y      # sq. distance from beam center along tilted plane
        z2 = z * z              # sq. distance from waist along centerline

        zr = pi * w0 * w0 / wl
        zr2 = zr * zr
        wz2 = w0 * w0 * (1 + z2 / zr2)
        wz = numpy.sqrt(wz2)

        k = 2 * pi / wl
        Rz = z * (1 + zr2 / z2)
        gouy = numpy.arctan(z / zr)

        gaussian = w0 / wz * exp(-r2 / wz2) * exp(1j * (k * z + k * r2 / 2 / Rz - gouy))
        # window_x = scipy.signal.windows.kaiser(xs.size, 14)
        # gaussian *= window_x[:, None, None]
        return gaussian

    zsEy = grid.shifted_xyz(1)[2]
    gaussianEy = grid2gaussian(grid.shifted_xyz(1), [0, 0, zsEy[m[2]]])

    normEy = gaussianEy[m[0]:-m[0], :, m[2]]
    gaussianEy /= numpy.sqrt((normEy[1].conj() * normEy[1]).sum())

    return gaussianEy


def run(pml=(10, 0, 10), dx=20, wl=1310, dwl=130, wg_zh=400, wg_x=-7500, fiber_z=1000, max_t=int(10e3)):
    omega = 2 * pi / wl

    x_min = -10e3 - pml[0] * dx
    x_max = 10e3 + pml[0] * dx
    z_min = -600 - pml[2] * dx
    z_max = 1400 + pml[2] * dx

    ex = numpy.arange(x_min, x_max + dx / 2, dx)
    ez = numpy.arange(z_min, z_max + dx / 2, dx)
    exyz = [ex, [-dx / 2, dx / 2], ez]
    grid = gridlock.Grid(exyz, periodic=True)
    epsilon = grid.allocate(1.45**2)

    def unvec(f):
        return meanas.fdmath.unvec(f, grid.shape)

#    grid.draw_slab(epsilon, surface_normal=2, center=[0, 0, 0], thickness=160, eps=3.5**2)


    e = numpy.zeros_like(epsilon, dtype=numpy.float32)
    h = numpy.zeros_like(epsilon, dtype=numpy.float32)

    dxes = [grid.dxyz, grid.autoshifted_dxyz()]
    min_dx = min(min(dxn) for dxn in chain(*dxes))
    dt = min_dx * .99 / numpy.sqrt(3)

    source_phasor, delay, n_fft = pulse(wl, dwl, dt)
    if 2 * delay / dt > max_t:
        raise Exception('Source extends beyond end of simulation')


    m = numpy.array(pml) + 10
    m[2] = grid.pos2ind([0, 0, fiber_z], which_shifts=0)[2] - grid.shape[2]

    ey_gauss = numpy.zeros_like(epsilon, dtype=complex)
    ey_gauss = get_gaussian(m, grid, dxes, wl / 1.45)
    e_gauss = numpy.zeros_like(epsilon, dtype=numpy.complex64)
    e_gauss[1] = ey_gauss
    mask = numpy.zeros_like(epsilon, dtype=int)
    mask[..., :m[2]] = 1
    src_op = operators.e_boundary_source(mask=vec(mask), omega=omega, dxes=dxes, epsilon=vec(epsilon))

    def zero_pmls(c):
        for a in range(3):
            c[a][:pml[0]+1, :, :] = 0
            c[a][-pml[0]-1:, :, :] = 0
            c[a][:, :, :pml[2]+1] = 0
            c[a][:, :, -pml[2]-1:] = 0
        return c

#    J = unvec(src_op @ vec(e_gauss))
#    J[:, :12, :, :] = 0
#    J[:, -12:, :, :] = 0
#    J[:, :, :, :12] = 0
#    J[:, :, :, -12:] = 0
#    zero_pmls(J)

    J = numpy.zeros_like(epsilon, dtype=complex)
    J[1, 500, 0, 60] = 1
    zero_pmls(J)

    half_dims = numpy.array([wg_x, dx, wg_zh])
    wg_args, wg_results = get_wgmode_xp(half_dims, -1, grid, wl, dxes)

    E_out = compute_overlap_e(E=wg_results['E'], wavenumber=wg_results['wavenumber'],
                              dxes=dxes, axis=0, polarity=+1, slices=wg_args['slices'])


    jr = (J.real / epsilon).astype(numpy.float32)
    ji = (J.imag / epsilon).astype(numpy.float32)


    eph = numpy.zeros_like(e, dtype=numpy.complex64)
    ephm = numpy.zeros_like(e, dtype=numpy.complex64)
#    powers = numpy.zeros((max_t, 5))
    p_ph = 0

    pml_params = [[cpml_params(axis=dd, polarity=pp, dt=dt,
                               thickness=pml[dd], epsilon_eff=1.0**2)
                   if pml[dd] > 0 else None
                   for pp in (-1, +1)]
                  for dd in range(3)]
    update_E, update_H = updates_with_cpml(cpml_params=pml_params, dt=dt,
                                           dxes=dxes, epsilon=epsilon)

    mov_interval = 10
    mov = numpy.empty((max_t // mov_interval, e.shape[1], e.shape[3]), dtype=numpy.float32)

    for t in range(max_t):
        update_E(e, h, epsilon)
        _, cm5, sm5 = source_phasor(t - 0.5)
        ephm += (cm5 - 1j * sm5) * e

        a, c, s = source_phasor(t)
        p_ph += a * c * c
        e -= (a * c) * jr - (a * s) * ji

        update_H(e, h)

        _, cp5, sp5 = source_phasor(t + 0.5)
        eph += (cp5 - 1j * sp5) * e

#        S = poynting(e, h, epsilon)
#
#        powers[t, :] = (
#            numpy.sum(S[2, m[0]+3:-m[0]-2, :, m[2]-6]), # below src
#            numpy.sum(S[2, m[0]+3:-m[0]-2, :, m[2]+4]), # above src
#            numpy.sum(S[2, m[0]+3:-m[0]-2, :, pml[2]+2]), # bottom
#            numpy.sum(S[0, +m[0]+2, :, pml[2]+3:m[2]+4]), # left
#            numpy.sum(S[0, -m[0]-2, :, pml[2]+3:m[2]+4]), # right
#            )

        if t % mov_interval == 0:
            mov[t // mov_interval] = e[1, :, 0, :].real

    eph *= dt / p_ph
    ephm *= dt / p_ph

    src_power = -(J * eph).real.sum() / 2 * dx ** 3

    hph = meanas.fdfd.functional.e2h(omega=omega, dxes=dxes)(eph)
    sph = meanas.fdtd.poynting(e=eph, h=hph.conj(), dxes=dxes)
    planes_powers = numpy.array((
        -sph[0,  11, :, 11:-12].sum(),
        +sph[0, -12, :, 11:-12].sum(),
        -sph[2, 11:-12, :,  11].sum(),
        +sph[2, 11:-12, :, -12].sum(),
        )).real / 2
    planes_power = planes_powers.sum()

    print(f'{src_power=}, {planes_power=}')


    # Verify
    A = meanas.fdfd.operators.e_full(omega=omega, dxes=dxes, epsilon=vec(epsilon))
    b = -1j * omega * vec(J) #* numpy.exp(1j * dt / 2 * omega)
    c = A @ vec(eph)
    logger.info('FWD inaccuracy: |Ax-b|/|b| = {}'.format(norm(c-b) / norm(b)))
    normdiv = norm(b) / norm(c)
    logger.info(f'{normdiv=}')
    logger.info('FWD renormed inaccuracy: |Ax-b|/|b| = {}'.format(norm(c * normdiv - b) / norm(b)))

    b = -1j * omega * vec(J)
    logger.info('FWD base inaccuracy: |Ax-b|/|b| = {}'.format(norm(c-b) / norm(b)))

    from scipy.optimize import minimize
    def resid(x):
        b = -1j * omega * vec(J) * numpy.exp(1j * dt * x * omega)
        return norm(c - b) / norm(b)
    print('min', minimize(resid, 0.25, options={'xatol': 1e-14, 'fatol': 1e-14}))

#    fig, ax, anim = plot_movie(mov, balanced=True, interval=300)
#    anim.save('output.mp4')

    print('solving...')
    cdxes = copy.deepcopy(dxes)
    for axis in range(3):
        thickness = pml[axis]
        if not thickness:
            continue
        for pp, polarity in enumerate((-1, 1)):
            print(axis, polarity, thickness)
            cdxes = fdfd.scpml.stretch_with_scpml(cdxes, axis=axis, polarity=polarity,
                                                  omega=omega, epsilon_effective=1.0**2,
                                                  thickness=thickness)
    eph2v = meanas.fdfd.solvers.generic(
        omega=omega, dxes=cdxes, J=vec(J), epsilon=vec(epsilon),
        matrix_solver_opts={'atol': 1e-3, 'tol': 1e-3, 'x0': vec(eph)})
    eph2 = unvec(eph2v)

    pyplot.figure()
    pyplot.pcolormesh(numpy.abs(eph/eph2)[1, 11:-11, 0, 11:-11].real.T)
    pyplot.colorbar()
    pyplot.title('mag')
    pyplot.figure()
    pyplot.pcolormesh(numpy.angle(eph/eph2)[1, 11:-11, 0, 11:-11].real.T)
    pyplot.colorbar()
    pyplot.title('angle')
    pyplot.show()
    breakpoint()


import matplotlib
from matplotlib import cycler, animation, colors, ticker, pyplot

def set_pyplot_cycle() -> None:
    pyplot.rc('lines', linewidth=2.5)
    pyplot.rc('axes', prop_cycle(
          cycler('color', 'krbgcm')
        * cycler('linestyle', ['-', '--', ':', '-.'])
        ))


def pcm(x, y, z, pca={}, cba={}, bare=False, eq=True) -> Tuple:
    z = numpy.array(z)

    if numpy.any(z < 0):
        vmax = numpy.abs(z).max()
        pcolor_args = {'vmin': -vmax, 'vmax': vmax, 'cmap': 'seismic', **pca}
    else:
        pcolor_args = {'cmap': 'seismic', **pca}

    xe = centers2edges(x)
    ye = centers2edges(y)

    if bare:
        fig = pyplot.gcf()
        ax = pyplot.gca()
    else:
        fig, ax = pyplot.subplot()

    im = ax.pcolormesh(xe, ye, z.T, **pcolor_args)
    if eq:
        ax.set_aspect('equal', adjustable='box')

    if not bare:
        ax.format_coord = lambda xx, yy: format_coord(xx, yy, xe, ye, z.T)
        fig.colorbar(im, ax=ax, **cba)

    return fig, ax, im


def pcc(x, y, z, cfa={}, cba={}, n_levels: int = 15, bare: bool = False, eq: bool = True) -> Tuple:
    z = numpy.array(z)

    if numpy.any(z < 0):
        vmax = numpy.abs(z).max()
        pcolor_args = {'vmin': -vmax, 'vmax': vmax, 'cmap': 'seismic', **cfa}
    else:
        pcolor_args = {'cmap': 'hot', **cfa}

    xe = centers2edges(x)
    ye = centers2edges(y)

    if bare:
        fig = pyplot.gcf()
        ax = pyplot.gca()
    else:
        fig, ax = pyplot.subplot()

    levels = ticker.MaxNLocator(nbins=n_levels).tick_values(z.min(), z.max())
    cmap = pyplot.get_cmap(pcolor_args['cmap'])
    norm = color.BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    im = ax.contourf(x, y, z.T, levels=levels, **pcolor_args)
    if eq:
        ax.set_aspect('equal', adjustable='box')

    if not bare:
        ax.format_coord = lambda xx, yy: format_coord(xx, yy, xe, ye, z.T)
        fig.colorbar(im, ax=ax, **cba)

    return fig, ax, im


def centers2edges(centers):
    d = numpy.diff(centers) / 2
    e = numpy.hstack((centers[0] - d[0], centers[:-1] + d, centers[-1] + d[-1]))
    return e


def format_coord(x, y, xs, ys, vs):
    col = numpy.digitize(x, xs)
    row = numpy.digitize(y, ys)
    if 0 < row <= vs.shape[0] and 0 < col <= vs.shape[1]:
        z = vs[row - 1, col - 1]
        return f'x={x:1.4g}, y={y:1.4g}, z={z:1.4g}'
    else:
        return f'x={x:1.4g}, y={y:1.4g}'


def plot_movie(arr, balanced=True, interval=300, pca={}):
    if balanced:
        vmax = numpy.abs(arr).max()
        pcolor_args = {'vmin': -vmax, 'vmax': vmax, 'cmap': 'seismic', **pca}
    else:
        pcolor_args = {'cmap': 'seismic', **pca}

    fig, ax = pyplot.subplots()
    im = ax.pcolormesh(arr[0, :, :].T, **pcolor_args)
    ax.set_aspect('equal', adjustable='box')

    def animate(ii):
        im.set_array(arr[ii, :, :].T.ravel())

    anim = animation.FuncAnimation(fig, animate, frames=arr.shape[0], repeat=True, interval=interval)
    return fig, im, anim


if __name__ == '__main__':
    run()
