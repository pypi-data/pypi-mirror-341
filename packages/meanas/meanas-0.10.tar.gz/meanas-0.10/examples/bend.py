import numpy
from numpy import pi
import gridlock
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
    numpy.arange(-1 * dx, 1 * dx + dx, dx)],
    periodic=True,
    )
epsilon = grid.allocate(eps_ox)

grid.draw_cuboid(epsilon, center=[x0, thf / 2, 0], dimensions=[width,       thf, 1e6], foreground=eps_si)
grid.draw_cuboid(epsilon, center=[x0, thp / 2, 0], dimensions=[width + 3e3, thp, 1e6], foreground=eps_si)
grid.draw_cuboid(epsilon, center=[x0 + width / 2 + 2e3, thf / 2, 0], dimensions=[1e3, thf, 1e6], foreground=eps_si)
grid.draw_cuboid(epsilon, center=[x0 - width / 2 - 2e3, thf / 2, 0], dimensions=[1e3, thf, 1e6], foreground=eps_si)


tilt = (1 + grid.xyz[0] / radius)
se = tilt[None, :, None, None] * epsilon
#print(tilt)


dxes = [grid.dxyz, grid.autoshifted_dxyz()]
dxes_2d = [[d[0], d[1]] for d in dxes]
mode_numbers = numpy.arange(6)
args = dict(dxes=dxes_2d, omega=omega, mode_numbers=numpy.arange(6))

e_xys, wavenumbers = waveguide_2d.solve_modes(epsilon=se[:, :, :, 1].ravel(), **args)
ee, hh = waveguide_2d.normalized_fields_e(e_xys[0], wavenumber=wavenumbers[0], dxes=dxes_2d, omega=omega, epsilon=se[:, :, :, 1].ravel())

#print('tilted baseline:' wavenumbers * wl / pi / 2)


rmin = radius + grid.xyz[0].min()
epsv = epsilon[:, :, :, 1].ravel()
e2, angular_wavenumbers2 = waveguide_cyl.solve_modes(epsilon=epsv, rmin=rmin, **args)
print('cylindrical:', angular_wavenumbers2 * wl / pi / 2 / radius)


wavenumbers_2 = waveguide_cyl.linear_wavenumbers(e_xys=e2, angular_wavenumbers=angular_wavenumbers2, rmin=rmin, epsilon=epsv, dxes=dxes_2d)
print('cyl_auto:', wavenumbers_2 * wl / pi / 2)


