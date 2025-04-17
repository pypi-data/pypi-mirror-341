import numpy
from numpy import pi
import gridlock
from gridlock import XYZExtent
from meanas.fdfd import waveguide_2d, waveguide_cyl
from matplotlib import pyplot


wl = 1310
dx = 10
radius = 25e3
width = 400
thf = 161
thp = 77
eps_si = 3.51 ** 2
eps_ox = 1.453 ** 2



x0 = (width / 2) % dx
omega = 2 * pi / wl

grid = gridlock.Grid([
    numpy.arange(-3000, 3000 + dx, dx),
    numpy.arange(-1500, 1500 + dx, dx),
    numpy.arange(-5 * dx, 5 * dx + dx, dx)],
    periodic=True,
    )
epsilon = grid.allocate(eps_ox)

grid.draw_cuboid(epsilon, extent=XYZExtent(xctr=x0, lx=width + 5e3, ymin=0, ymax=thf, zmin=-1e6, zmax=0), foreground=eps_si)
grid.draw_cuboid(epsilon, extent=XYZExtent(xmax=-width / 2, lx=1.5e3, ymin=thp, ymax=1e6, zmin=-1e6, zmax=0), foreground=eps_ox)
grid.draw_cuboid(epsilon, extent=XYZExtent(xmin= width / 2, lx=1.5e3, ymin=thp, ymax=1e6, zmin=-1e6, zmax=0), foreground=eps_ox)

grid.draw_cuboid(epsilon, extent=XYZExtent(xmax=-(width / 2 + 2.5e3), lx=1e3, ymin=0, ymax=thf, zmin=0, zmax=1e6), foreground=eps_si)
grid.draw_cuboid(epsilon, extent=XYZExtent(xmax=  width / 2 + 2.5e3,  lx=1e3, ymin=0, ymax=thf, zmin=0, zmax=1e6), foreground=eps_si)


dxes = [grid.dxyz, grid.autoshifted_dxyz()]
dxes_2d = [[d[0], d[1]] for d in dxes]
mode_numbers = numpy.arange(20)
args = dict(dxes=dxes_2d, omega=omega, mode_numbers=mode_numbers)

eps1 = epsilon[:, :, :,  1].ravel()
eps2 = epsilon[:, :, :, -2].ravel()
eL_xys, wavenumbers_L = waveguide_2d.solve_modes(epsilon=eps1, **args)
eR_xys, wavenumbers_R = waveguide_2d.solve_modes(epsilon=eps2, **args)
eh_L = [
    waveguide_2d.normalized_fields_e(e_xy, wavenumber=wavenumber, dxes=dxes_2d, omega=omega, epsilon=eps1)
    for e_xy, wavenumber in zip(eL_xys, wavenumbers_L)]
eh_R = [
    waveguide_2d.normalized_fields_e(e_xy, wavenumber=wavenumber, dxes=dxes_2d, omega=omega, epsilon=eps2)
    for e_xy, wavenumber in zip(eR_xys, wavenumbers_R)]


eh_R = [
    waveguide_2d.normalized_fields_e(e_xy, wavenumber=wavenumber, dxes=dxes_2d, omega=omega, epsilon=eps2)
    for e_xy, wavenumber in zip(eR_xys, wavenumbers_R)]


ss = waveguide_2d.get_s(eh_L, wavenumbers_L, eh_R, wavenumbers_R, dxes=dxes_2d)

ss11 = waveguide_2d.get_s(eh_L, wavenumbers_L, eh_L, wavenumbers_L, dxes=dxes_2d)
ss22 = waveguide_2d.get_s(eh_R, wavenumbers_R, eh_R, wavenumbers_R, dxes=dxes_2d)

