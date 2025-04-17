import numpy
from numpy import pi
import gridlock
from gridlock import XYZExtent
from meanas.fdfd import waveguide_2d, waveguide_cyl
from meanas.fdmath import vec, unvec
from matplotlib import pyplot, colors
from scipy import sparse
import skrf
from skrf import Network


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
grid.draw_cuboid(epsilon, extent=XYZExtent(xmax=-width / 2, lx=1.5e3, ymin=thp, ymax=1e6, zmin=-1e6, zctr=0), foreground=eps_ox)
grid.draw_cuboid(epsilon, extent=XYZExtent(xmin= width / 2, lx=1.5e3, ymin=thp, ymax=1e6, zmin=-1e6, zctr=0), foreground=eps_ox)


dxes = [grid.dxyz, grid.autoshifted_dxyz()]
dxes_2d = [[d[0], d[1]] for d in dxes]
mode_numbers = numpy.arange(20)
args = dict(dxes=dxes_2d, omega=omega, mode_numbers=mode_numbers)

eps = epsilon[:, :, :, 2].ravel()
rmin = radius + grid.xyz[0].min()
eL_xys, wavenumbers_L = waveguide_2d.solve_modes(epsilon=eps, **args)
eR_xys, ang_wavenumbers_R = waveguide_cyl.solve_modes(epsilon=eps, **args, rmin=rmin)
linear_wavenumbers_R = waveguide_cyl.linear_wavenumbers(e_xys=eR_xys, angular_wavenumbers=ang_wavenumbers_R, rmin=rmin, epsilon=eps, dxes=dxes_2d)

eh_L = [
    waveguide_2d.normalized_fields_e(e_xy, wavenumber=wavenumber, dxes=dxes_2d, omega=omega, epsilon=eps)
    for e_xy, wavenumber in zip(eL_xys, wavenumbers_L)]
eh_R = [
    waveguide_cyl.normalized_fields_e(e_xy, angular_wavenumber=ang_wavenumber, dxes=dxes_2d, omega=omega, epsilon=eps, rmin=rmin)
    for e_xy, ang_wavenumber in zip(eR_xys, ang_wavenumbers_R)]


ss = waveguide_2d.get_s(eh_L, wavenumbers_L, eh_R, linear_wavenumbers_R, dxes=dxes_2d)

ss11 = waveguide_2d.get_s(eh_L,        wavenumbers_L, eh_L,        wavenumbers_L, dxes=dxes_2d)
ss22 = waveguide_2d.get_s(eh_R, linear_wavenumbers_R, eh_R, linear_wavenumbers_R, dxes=dxes_2d)


fig, axes = pyplot.subplots(2, 2)
mb0 = axes[0, 0].pcolormesh(numpy.abs(ss[::-1])**2, cmap='hot', vmin=0)
fig.colorbar(mb0)
axes[1, 0].set_title('S Abs^2')
mb2 = axes[1, 0].pcolormesh(ss[::-1].real, cmap='bwr', norm=colors.CenteredNorm())
fig.colorbar(mb2)
axes[1, 0].set_title('S Real')
mb3 = axes[1, 1].pcolormesh(ss[::-1].imag, cmap='bwr', norm=colors.CenteredNorm())
fig.colorbar(mb3)
axes[1, 1].set_title('S Imag')
pyplot.show(block=False)

e1, h1 = eh_L[2]
e2, h2 = eh_R[2]

figE, axesE = pyplot.subplots(3, 2)
figH, axesH = pyplot.subplots(3, 2)
esqmax = max(numpy.abs(e1).max(), numpy.abs(e2).max()) ** 2
hsqmax = max(numpy.abs(h1).max(), numpy.abs(h2).max()) ** 2
for mm, (ee, hh) in enumerate(zip((e1, e2), (h1, h2))):
    E = unvec(ee, grid.shape[:2])
    H = unvec(hh, grid.shape[:2])
    for aa in range(3):
        axesE[aa, mm].pcolormesh((numpy.abs(E[aa]) ** 2).T, cmap='bwr', norm=colors.CenteredNorm(halfrange=esqmax))
        axesH[aa, mm].pcolormesh((numpy.abs(H[aa]) ** 2).T, cmap='bwr', norm=colors.CenteredNorm(halfrange=hsqmax))
pyplot.show(block=False)



net_wb = Network(f=[1 / wl], s = ss)
net_bw = net_wb.copy()
net_bw.renumber(numpy.arange(40), numpy.roll(numpy.arange(40), 20))

wg_phase = sparse.diags_array(numpy.exp(-1j * wavenumbers_L * 100e3))
bend_phase = sparse.diags_array(numpy.exp(-1j * ang_wavenumbers_R * pi / 2))
net_propwg = Network(f=[1 / wl], s = sparse.block_array(([None, wg_phase], [wg_phase, None])).toarray()[None, ...])
net_propbend = Network(f=[1 / wl], s = sparse.block_array(([None, bend_phase], [bend_phase, None])).toarray()[None, ...])


cir = skrf.network.cascade_list([net_propwg, net_wb, net_propbend, net_bw, net_propwg])

