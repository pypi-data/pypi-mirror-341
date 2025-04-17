"""
Example Ge waveguide modesolve
"""
import logging

import numpy
from matplotlib import pyplot, colors

import gridlock
import meanas
from meanas.fdmath import fdfield_t
from meanas.fdfd import waveguide_3d


logging.basicConfig(level=logging.DEBUG)
for pp in ('matplotlib', 'PIL'):
    logging.getLogger(pp).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def draw_grid(
        *,
        dx: float,
        n_wg: float = 4.0,  # Ge
        n_cladding: float = 1.00,    # Air index
        wg_w: float = 700,
        wg_th: float = 200,
        ) -> tuple[gridlock.Grid, fdfield_t]:
    """ Create the grid and draw the device  """
    # Half-dimensions of the simulation grid
    xyz_max = numpy.array([dx / 2, 900, 600])

    # Coordinates of the edges of the cells.
    half_edge_coords = [numpy.arange(dx / 2, m + dx / 2, step=dx) for m in xyz_max]
    edge_coords = [numpy.hstack((-h[::-1], h)) for h in half_edge_coords]

    grid = gridlock.Grid(edge_coords)
    epsilon = grid.allocate(n_cladding ** 2, dtype=numpy.float32)
    grid.draw_cuboid(
        epsilon,
        foreground = n_wg ** 2,
        x = dict(center=0, span=8e3),
        y = dict(center=0, span=wg_w),
        z = dict(center=0, span=wg_th),
        )

    return grid, epsilon


def main(
        *,
        dx: float = 20,                  # discretization (nm / cell)
        wl: float = 2000,                # Excitation wavelength
        wg_w: float = 700,               # Waveguide width
        wg_th: float = 200,              # Waveguide thickness
        ):
    omega = 2 * numpy.pi / wl

    # Draw a 3D grid
    grid, epsilon = draw_grid(dx=dx)

    # Grab a 2D region for the waveguide sim
    slices = [slice(0, 1), slice(0, -1), slice(0, -1)]

    wg_args = dict(
        slices = slices,
        dxes = [grid.dxyz, grid.autoshifted_dxyz()],
        axis = 0,
        polarity = +1,
        )

    wg_results = waveguide_3d.solve_mode(mode_number=0, omega=omega, epsilon=epsilon, **wg_args)

    ee = wg_results['E']
    x0 = grid.xyz[slices[0]]
    fig, ax = grid.visualize_slice(
        ee.real,
        plane = dict(x=x0),
        which_shifts = 1,
        finalize = False,
        pcolormesh_args = dict(norm = colors.CenteredNorm(), cmap='bwr'),
        )
    ax.set_title('$E_y$')
    pyplot.show(block=True)


if __name__ == '__main__':
    main()
