import logging
import meanas
from meanas.fdfd.scpml import stretch_with_scpml
from meanas.fdfd.solvers import generic
from meanas.fdtd.misc import gaussian_beam
from meanas.fdmath import vec
from gridlock import Grid
import numpy
from numpy import pi
from matplotlib import pyplot, colors


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
for mm in ('matplotlib', 'PIL'):
    logging.getLogger(mm).setLevel(logging.WARNING)


wl = 1310
omega = 2 * pi / wl
eps_bg = 1.45

grid = Grid([
    numpy.arange(-20e3, 20e3 + 1, 10),
    [-1, 1],
    numpy.arange(-1e3, 1e3 + 1, 10),
    ])

logger.info(grid.shape)
def unvec(vv):
    return meanas.fdmath.unvec(vv, grid.shape)

eps = grid.allocate(eps_bg)
dxes = [grid.dxyz, grid.autoshifted_dxyz()]

xx, yy, zz = grid.shifted_xyz(1)
print(zz.min(), zz.max(), zz[-25])
gauss0 = gaussian_beam(xyz=[xx[12:-12], yy, zz], center=[0, 0, zz[-25]], w0=4600, tilt=numpy.deg2rad(-10), wl=wl / eps_bg)

e_gauss = numpy.zeros_like(eps, dtype=complex)
e_gauss[1, 12:-12, :, :] = gauss0
mask = numpy.zeros_like(eps)
mask[..., :-25] = 1

fig, ax = pyplot.subplots()
mb = ax.pcolormesh(mask[0, :, 0, :].T, cmap='hot')
fig.colorbar(mb)
ax.set_aspect('equal')
ax.set_title('mask')

fig, ax = pyplot.subplots()
mb = ax.pcolormesh((e_gauss * mask)[1, :, 0, :].real.T, cmap='bwr', norm=colors.CenteredNorm())
fig.colorbar(mb)
ax.set_aspect('equal')
ax.set_title('e_masked')

pyplot.show()

vecJ = meanas.fdfd.operators.e_boundary_source(mask=vec(mask), omega=omega, dxes=dxes, epsilon=vec(eps)) @ vec(e_gauss)
J = unvec(vecJ)

for pp in (-1, +1):
    for aa in (0, 2):
        dxes = stretch_with_scpml(
            dxes=dxes,
            axis=aa,
            polarity=pp,
            omega=omega,
            thickness=10,
            )

vecE = generic(omega=omega, dxes=dxes, J=vec(J), epsilon=vec(eps))
vecH = meanas.fdfd.operators.e2h(omega=omega, dxes=dxes) @ vecE
vecS = meanas.fdfd.operators.poynting_e_cross(e=vecE, dxes=dxes) @ vecH.conj()

E = unvec(vecE)
H = unvec(vecH)
S = unvec(vecS)
dxs, dys, dzs = grid.dxyz
EJ = (-E * J.conj()).sum(axis=0) * dxs[:, None, None] * dys[None, : None] * dzs[None, None, :]
P_in = EJ.sum().real / 2

logger.info(f'P_in = {EJ.sum() / 2:3g}')

planes = numpy.array([
    -S[0,  11, :, :].sum(),
     S[0, -11, :, :].sum(),
    -S[2, :, :,  11].sum(),
     S[2, :, :, -11].sum(),
     ]) / 2 / P_in

logger.info(f'{planes=}')
logger.info(f'{planes.sum().real}')


fig, ax = pyplot.subplots()
e2 = (E * E.conj() * eps).real.sum(axis=0)
mb = ax.pcolormesh(e2[:, 0, :].T / P_in, cmap='hot', norm=colors.LogNorm(vmin=e2.max() / 1e10))
fig.colorbar(mb)
ax.set_aspect('equal')
ax.set_title('E^2 * eps')

fig, ax = pyplot.subplots()
mb = ax.pcolormesh(S[0, :, 0, :].real.T / 2 / P_in, cmap='bwr', norm=colors.CenteredNorm())
fig.colorbar(mb)
ax.set_aspect('equal')
ax.set_title('Sx')

fig, ax = pyplot.subplots()
mb = ax.pcolormesh(S[2, :, 0, :].real.T / 2 / P_in, cmap='bwr', norm=colors.CenteredNorm())
fig.colorbar(mb)
ax.set_aspect('equal')
ax.set_title('Sz')

fig, ax = pyplot.subplots()
mb = ax.pcolormesh(EJ[:, 0, :].real.T / 2 / P_in, cmap='bwr', norm=colors.CenteredNorm())
fig.colorbar(mb)
ax.set_aspect('equal')
ax.set_title('-E.J')

pyplot.show()
