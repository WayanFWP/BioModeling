from library.Function import Function
from library.Gui import *

# example usage
f1 = 0.1
f2 = 0.25
c1, c2 = 0.01, 0.01
Nrr = 256
S_f = Function.loop_gausian(Nrr, f1, f2, c1, c2)
real, imag = Function.idft(S_f)
S = (real + imag) * 2
S = Function.scaling(S)

sideBySide(S_f, S)