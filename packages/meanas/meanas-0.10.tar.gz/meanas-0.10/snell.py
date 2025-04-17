import numpy
def snell_s(n1, n2, theta):
    aa = n1 / n2 * numpy.sin(theta)
    bb = n1 * cos(theta)
    r0 = (bb - n2 * numpy.sqrt(1 - aa * aa)) / (bb + n2 * numpy.sqrt(1 - aa * aa))
    return numpy.real(r0 * numpy.conj(r0))
def snell_p(n1, n2, theta):
    aa = n1 / n2 * numpy.sin(theta)
    qq = n1 * numpy.sqrt(1 - aa * aa)
    cc = n2 * numpy.cos(theta)
    r0 = (qq - cc) / (qq + cc)
    return numpy.real(r0 * numpy.conj(r0))
def snell_s(n1, n2, theta):
    aa = n1 / n2 * numpy.sin(theta)
    qq = n2 * numpy.sqrt(1 - aa * aa)
    bb = n1 * cos(theta)
    r0 = (bb - qq) / (bb + qq)
    return numpy.real(r0 * numpy.conj(r0))
snell_s(1.45, 3.4, numpy.deg2rad(10))
def snell_s(n1, n2, theta):
    aa = n1 / n2 * numpy.sin(theta)
    qq = n2 * numpy.sqrt(1 - aa * aa)
    bb = n1 * numpy.cos(theta)
    r0 = (bb - qq) / (bb + qq)
    return numpy.real(r0 * numpy.conj(r0))
snell_s(1.45, 3.4, numpy.deg2rad(10))
snell_p(1.45, 3.4, numpy.deg2rad(10))
def snell_s_tdb(n1, n2, theta):
    rr = snell_s(n1, n2, theta)
    return 10 * numpy.log10(1 - rr)
def snell_p_tdb(n1, n2, theta):
    rr = snell_p(n1, n2, theta)
    return 10 * numpy.log10(1 - rr)
snell_s_tdb(1.0, 3.4, numpy.deg2rad(10)) + snell_s_tdb(1.45, 3.4, numpy.arcsin(numpy.sin(numpy.deg2rad(10)) * 1 / 3.4))
snell_p_tdb(1.0, 3.4, numpy.deg2rad(10)) + snell_p_tdb(1.45, 3.4, numpy.arcsin(numpy.sin(numpy.deg2rad(10)) * 1 / 3.4))
%history -f /home/jan/projects/meanas/snell.py
