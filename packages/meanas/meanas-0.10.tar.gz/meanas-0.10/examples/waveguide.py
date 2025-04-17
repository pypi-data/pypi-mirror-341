"""
Example code for running an OpenCL FDTD simulation

See main() for simulation setup.
"""
from typing import Callable
import logging
import time
import copy

import numpy
import h5py
from numpy.linalg import norm

import gridlock
import meanas
from meanas import fdtd, fdfd
from meanas.fdtd import cpml_params, updates_with_cpml
from meanas.fdtd.misc import gaussian_packet

from meanas.fdmath import vec, unvec, vcfdfield_t, cfdfield_t, fdfield_t, dx_lists_t
from meanas.fdfd import waveguide_3d, functional, scpml, operators
from meanas.fdfd.solvers import generic as generic_solver
from meanas.fdfd.operators import e_full
from meanas.fdfd.scpml import stretch_with_scpml


logging.basicConfig(level=logging.DEBUG)
for pp in ('matplotlib', 'PIL'):
    logging.getLogger(pp).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def pcolor(vv, fig=None, ax=None) -> None:
    if fig is None:
        assert ax is None
        fig, ax = pyplot.subplots()
    mb = ax.pcolor(vv, cmap='seismic', norm=colors.CenteredNorm())
    fig.colorbar(mb)
    ax.set_aspect('equal')


def draw_grid(
        *,
        dx: float,
        pml_thickness: int,
        n_wg: float = 3.476,        # Si index @ 1550
        n_cladding: float = 1.00,    # Air index
        wg_w: float = 400,
        wg_th: float = 200,
        ) -> tuple[gridlock.Grid, fdfield_t]:
    """ Create the grid and draw the device  """
    # Half-dimensions of the simulation grid
    xyz_max = numpy.array([800, 900, 600]) + (pml_thickness + 2) * dx

    # Coordinates of the edges of the cells.
    half_edge_coords = [numpy.arange(dx / 2, m + dx / 2, step=dx) for m in xyz_max]
    edge_coords = [numpy.hstack((-h[::-1], h)) for h in half_edge_coords]

    grid = gridlock.Grid(edge_coords)
    epsilon = grid.allocate(n_cladding**2, dtype=numpy.float32)
    grid.draw_cuboid(
        epsilon,
        x = dict(center=0, span=8e3),
        y = dict(center=0, span=wg_w),
        z = dict(center=0, span=wg_th),
        foreground = n_wg ** 2,
        )

    return grid, epsilon


def get_waveguide_mode(
        *,
        grid: gridlock.Grid,
        dxes: dx_lists_t,
        omega: float,
        epsilon: fdfield_t,
        ) -> tuple[vcfdfield_t, vcfdfield_t]:
    """ Create a mode source and overlap window """
    dims = numpy.array([[-10, -20, -15],
                        [-10,  20,  15]]) * [[numpy.median(numpy.real(dx)) for dx in dxes[0]]]
    ind_dims = (grid.pos2ind(dims[0], which_shifts=None).astype(int),
                grid.pos2ind(dims[1], which_shifts=None).astype(int))
    wg_args = dict(
        slices = [slice(i, f+1) for i, f in zip(*ind_dims)],
        dxes = dxes,
        axis = 0,
        polarity = +1,
        )

    wg_results = waveguide_3d.solve_mode(mode_number=0, omega=omega, epsilon=epsilon, **wg_args)
    J = waveguide_3d.compute_source(E=wg_results['E'], wavenumber=wg_results['wavenumber'],
                                    omega=omega, epsilon=epsilon, **wg_args)

    e_overlap = waveguide_3d.compute_overlap_e(E=wg_results['E'], wavenumber=wg_results['wavenumber'], **wg_args, omega=omega)
    return J, e_overlap


def main(
        *,
        solver: Callable = generic_solver,
        dx: float = 40,                  # discretization (nm / cell)
        pml_thickness: int = 10,         # (number of cells)
        wl: float = 1550,                # Excitation wavelength
        wg_w: float = 600,               # Waveguide width
        wg_th: float = 220,              # Waveguide thickness
        ):
    omega = 2 * numpy.pi / wl

    grid, epsilon = draw_grid(dx=dx, pml_thickness=pml_thickness)

    # Add PML
    dxes = [grid.dxyz, grid.autoshifted_dxyz()]
    for a in (0, 1, 2):
        for p in (-1, 1):
            dxes = scpml.stretch_with_scpml(dxes, omega=omega, axis=a, polarity=p, thickness=pml_thickness)


    J, e_overlap = get_waveguide_mode(grid=grid, dxes=dxes, omega=omega, epsilon=epsilon)


    pecg = numpy.zeros_like(epsilon)
    # pecg.draw_cuboid(pecg, center=[700, 0, 0], dimensions=[80, 1e8, 1e8], eps=1)
    # pecg.visualize_isosurface(pecg)

    pmcg = numpy.zeros_like(epsilon)
    # grid.draw_cuboid(pmcg, center=[700, 0, 0], dimensions=[80, 1e8, 1e8], eps=1)
    # grid.visualize_isosurface(pmcg)


#    ss = (1, slice(None), J.shape[2]//2+6, slice(None))
#    pcolor(J3[ss].T.imag)
#    pcolor((numpy.abs(J3).sum(axis=(0, 2)) > 0).astype(float).T)
#    pyplot.show(block=True)

    E_fdfd = fdfd_solve(
        omega = omega,
        dxes = dxes,
        epsilon = epsilon,
        J = J,
        pec = pecg,
        pmc = pmcg,
        )


    #
    # Plot results
    #
    center = grid.pos2ind([0, 0, 0], None).astype(int)
    fig, axes = pyplot.subplots(2, 2)
    pcolor(numpy.real(E[1][center[0], :, :]).T, fig=fig, ax=axes[0, 0])
    axes[0, 1].plot(numpy.log10(numpy.abs(E[1][:, center[1], center[2]]) + 1e-10))
    axes[0, 1].grid(alpha=0.6)
    axes[0, 1].set_ylabel('log10 of field')
    pcolor(numpy.real(E[1][:, :, center[2]]).T, fig=fig, ax=axes[1, 0])

    def poyntings(E):
        H = functional.e2h(omega, dxes)(E)
        poynting = fdtd.poynting(e=E, h=H.conj(), dxes=dxes)
        cross1 = operators.poynting_e_cross(vec(E), dxes) @ vec(H).conj()
        cross2 = operators.poynting_h_cross(vec(H), dxes) @ vec(E).conj() * -1
        s1 = 0.5 * unvec(numpy.real(cross1), grid.shape)
        s2 = 0.5 * unvec(numpy.real(cross2), grid.shape)
        s0 = 0.5 * poynting.real
#        s2 = poynting.imag
        return s0, s1, s2

    s0x, s1x, s2x = poyntings(E)
    axes[1, 1].plot(s0x[0].sum(axis=2).sum(axis=1), label='s0', marker='.')
    axes[1, 1].plot(s1x[0].sum(axis=2).sum(axis=1), label='s1', marker='.')
    axes[1, 1].plot(s2x[0].sum(axis=2).sum(axis=1), label='s2', marker='.')
    axes[1, 1].plot(E[1][:, center[1], center[2]].real.T, label='Ey', marker='x')
    axes[1, 1].grid(alpha=0.6)
    axes[1, 1].legend()

    q = []
    for i in range(-5, 30):
        e_ovl_rolled = numpy.roll(e_overlap, i, axis=1)
        q += [numpy.abs(vec(E) @ vec(e_ovl_rolled).conj())]
    fig, ax = pyplot.subplots()
    ax.plot(q, marker='.')
    ax.grid(alpha=0.6)
    ax.set_title('Overlap with mode')

    logger.info('Average overlap with mode:', sum(q[8:32]) / len(q[8:32]))

    pyplot.show(block=True)


def fdfd_solve(
        *,
        omega: float,
        dxes = dx_lists_t,
        epsilon: fdfield_t,
        J: cfdfield_t,
        pec: fdfield_t,
        pmc: fdfield_t,
        ) -> cfdfield_t:
    """ Construct and run the solve """
    sim_args = dict(
        omega = omega,
        dxes = dxes,
        epsilon = vec(epsilon),
        pec = vec(pecg),
        pmc = vec(pmcg),
        )

    x = solver(J=vec(J), **sim_args)

    b = -1j * omega * vec(J)
    A = operators.e_full(**sim_args).tocsr()
    logger.info('Norm of the residual is ', norm(A @ x - b) / norm(b))

    E = unvec(x, epsilon.shape[1:])
    return E


def main2():
    dtype = numpy.float32
    max_t = 3600            # number of timesteps

    dx = 40                 # discretization (nm/cell)
    pml_thickness = 8       # (number of cells)

    wl = 1550               # Excitation wavelength and fwhm
    dwl = 100

    # Device design parameters
    xy_size = numpy.array([10, 10])
    a = 430
    r = 0.285
    th = 170

    # refractive indices
    n_slab = 3.408  # InGaAsP(80, 50) @ 1550nm
    n_cladding = 1.0        # air

    # Half-dimensions of the simulation grid
    xy_max = (xy_size + 1) * a * [1, numpy.sqrt(3)/2]
    z_max = 1.6 * a
    xyz_max = numpy.hstack((xy_max, z_max)) + pml_thickness * dx

    # Coordinates of the edges of the cells. The fdtd package can only do square grids at the moment.
    half_edge_coords = [numpy.arange(dx/2, m + dx, step=dx) for m in xyz_max]
    edge_coords = [numpy.hstack((-h[::-1], h)) for h in half_edge_coords]

    # #### Create the grid, mask, and draw the device ####
    grid = gridlock.Grid(edge_coords)
    epsilon = grid.allocate(n_cladding ** 2, dtype=dtype)
    grid.draw_slab(
        epsilon,
        slab = dict(axis='z', center=0, span=th),
        foreground = n_slab ** 2,
        )


    print(f'{grid.shape=}')

    dt = dx * 0.99 / numpy.sqrt(3)
    ee = numpy.zeros_like(epsilon, dtype=dtype)
    hh = numpy.zeros_like(epsilon, dtype=dtype)

    dxes = [grid.dxyz, grid.autoshifted_dxyz()]

    # PMLs in every direction
    pml_params = [
        [cpml_params(axis=dd, polarity=pp, dt=dt, thickness=pml_thickness, epsilon_eff=n_cladding ** 2)
         for pp in (-1, +1)]
        for dd in range(3)]
    update_E, update_H = updates_with_cpml(cpml_params=pml_params, dt=dt, dxes=dxes, epsilon=epsilon)

    # sample_interval = numpy.floor(1 / (2 * 1 / wl * dt)).astype(int)
    # print(f'Save time interval would be {sample_interval} * dt = {sample_interval * dt:3g}')


    # Source parameters and function
    source_phasor, _delay = gaussian_packet(wl=wl, dwl=100, dt=dt, turn_on=1e-5)
    aa, cc, ss = source_phasor(numpy.arange(max_t))
    srca_real = aa * cc
    src_maxt = numpy.argwhere(numpy.diff(aa < 1e-5))[-1]
    assert aa[src_maxt - 1] >= 1e-5
    phasor_norm = dt / (aa * cc * cc).sum()

    Jph = numpy.zeros_like(epsilon, dtype=complex)
    Jph[1, *(grid.shape // 2)] = epsilon[1, *(grid.shape // 2)]
    Eph = numpy.zeros_like(Jph)

    # #### Run a bunch of iterations ####
    output_file = h5py.File('simulation_output.h5', 'w')
    start = time.perf_counter()
    for tt in range(max_t):
        update_E(ee, hh, epsilon)

        if tt < src_maxt:
            ee[1, *(grid.shape // 2)] -= srca_real[tt]
        update_H(ee, hh)

        avg_rate = (tt + 1) / (time.perf_counter() - start)

        if tt % 200 == 0:
            print(f'iteration {tt}: average {avg_rate} iterations per sec')
            E_energy_sum = (ee * ee * epsilon).sum()
            print(f'{E_energy_sum=}')

        # Save field slices
        if (tt % 20 == 0 and (max_t - tt <= 1000 or tt <= 2000)) or tt == max_t - 1:
            print(f'saving E-field at iteration {tt}')
            output_file[f'/E_t{tt}'] = ee[:, :, :, ee.shape[3] // 2]

        Eph += (cc[tt] - 1j * ss[tt]) * phasor_norm * ee

    omega = 2 * numpy.pi / wl
    Eph *= numpy.exp(-1j * dt / 2 * omega)
    b = -1j * omega * Jph
    dxes_fdfd = copy.deepcopy(dxes)
    for pp in (-1, +1):
        for dd in range(3):
            stretch_with_scpml(dxes_fdfd, axis=dd, polarity=pp, omega=omega, epsilon_effective=n_cladding ** 2, thickness=pml_thickness)
    A = e_full(omega=omega, dxes=dxes, epsilon=epsilon)
    residual = norm(A @ vec(ee) - vec(b)) / norm(vec(b))
    print(f'FDFD residual is {residual}')


if __name__ == '__main__':
    main()
