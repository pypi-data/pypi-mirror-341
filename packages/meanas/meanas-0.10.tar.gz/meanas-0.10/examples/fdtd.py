"""
Example code for running an FDTD simulation

See main() for simulation setup.
"""

import sys
import time
import copy

import numpy
import h5py
from numpy.linalg import norm

from meanas import fdtd
from meanas.fdtd import cpml_params, updates_with_cpml
from meanas.fdtd.misc import gaussian_packet

from meanas.fdfd.operators import e_full
from meanas.fdfd.scpml import stretch_with_scpml
from meanas.fdmath import vec
from masque import Pattern, Circle, Polygon
import gridlock
import pcgen


def perturbed_l3(a: float, radius: float, **kwargs) -> Pattern:
    """
    Generate a masque.Pattern object containing a perturbed L3 cavity.

    Args:
        a: Lattice constant.
        radius: Hole radius, in units of a (lattice constant).
        **kwargs: Keyword arguments:
        hole_dose, trench_dose, hole_layer, trench_layer: Shape properties for Pattern.
                Defaults *_dose=1, hole_layer=0, trench_layer=1.
        shifts_a, shifts_r: passed to pcgen.l3_shift; specifies lattice constant (1 -
                multiplicative factor) and radius (multiplicative factor) for shifting
                holes adjacent to the defect (same row). Defaults are 0.15 shift for
                first hole, 0.075 shift for third hole, and no radius change.
        xy_size: [x, y] number of mirror periods in each direction; total size is
                `2 * n + 1` holes in each direction. Default `[10, 10]`.
        perturbed_radius: radius of holes perturbed to form an upwards-driected beam
                (multiplicative factor). Default 1.1.
        trench width: Width of the undercut trenches. Default 1.2e3.

    Return:
        `masque.Pattern` object containing the L3 design
    """

    default_args = {
        'hole_layer':   0,
        'trench_layer': 1,
        'shifts_a':     (0.15, 0, 0.075),
        'shifts_r':     (1.0, 1.0, 1.0),
        'xy_size':      (10, 10),
        'perturbed_radius': 1.1,
        'trench_width': 1.2e3,
        }
    kwargs = {**default_args, **kwargs}

    xyr = pcgen.l3_shift_perturbed_defect(
        mirror_dims=kwargs['xy_size'],
        perturbed_radius=kwargs['perturbed_radius'],
        shifts_a=kwargs['shifts_a'],
        shifts_r=kwargs['shifts_r'],
        )
    xyr *= a
    xyr[:, 2] *= radius

    pat = Pattern()
    #pat.name = f'L3p-a{a:g}r{radius:g}rp{kwargs["perturbed_radius"]:g}'
    pat.shapes[(kwargs['hole_layer'], 0)] += [
        Circle(radius=r, offset=(x, y))
        for x, y, r in xyr]

    maxes = numpy.max(numpy.fabs(xyr), axis=0)
    pat.shapes[(kwargs['trench_layer'], 0)] += [
        Polygon.rectangle(
            lx=(2 * maxes[0]), ly=kwargs['trench_width'],
            offset=(0, s * (maxes[1] + a + kwargs['trench_width'] / 2))
            )
        for s in (-1, 1)]
    return pat


def main():
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
    n_air = 1.0   # air

    # Half-dimensions of the simulation grid
    xy_max = (xy_size + 1) * a * [1, numpy.sqrt(3)/2]
    z_max = 1.6 * a
    xyz_max = numpy.hstack((xy_max, z_max)) + pml_thickness * dx

    # Coordinates of the edges of the cells. The fdtd package can only do square grids at the moment.
    half_edge_coords = [numpy.arange(dx/2, m + dx, step=dx) for m in xyz_max]
    edge_coords = [numpy.hstack((-h[::-1], h)) for h in half_edge_coords]

    # #### Create the grid, mask, and draw the device ####
    grid = gridlock.Grid(edge_coords)
    epsilon = grid.allocate(n_air ** 2, dtype=dtype)
    grid.draw_slab(
        epsilon,
        slab = dict(axis='z', center=0, span=th),
        foreground = n_slab ** 2,
        )

    mask = perturbed_l3(a, r)
    grid.draw_polygons(
        epsilon,
        slab = dict(axis='z', center=0, span=2 * th),
        foreground = n_air ** 2,
        offset2d = (0, 0),
        polygons = mask.as_polygons(library=None),
        )

    print(f'{grid.shape=}')

    dt = dx * 0.99 / numpy.sqrt(3)
    ee = numpy.zeros_like(epsilon, dtype=dtype)
    hh = numpy.zeros_like(epsilon, dtype=dtype)

    dxes = [grid.dxyz, grid.autoshifted_dxyz()]

    # PMLs in every direction
    pml_params = [
        [cpml_params(axis=dd, polarity=pp, dt=dt, thickness=pml_thickness, epsilon_eff=n_air ** 2)
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
        sys.stdout.flush()

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
            stretch_with_scpml(dxes_fdfd, axis=dd, polarity=pp, omega=omega, epsilon_effective=n_air ** 2, thickness=pml_thickness)
    A = e_full(omega=omega, dxes=dxes, epsilon=epsilon)
    residual = norm(A @ vec(ee) - vec(b)) / norm(vec(b))
    print(f'FDFD residual is {residual}')


if __name__ == '__main__':
    main()
