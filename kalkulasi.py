from library.Function import Function
from library.Gui import *
from library.Variable import *

# step 1
f1 = 0.1
f2 = 0.25
c1, c2 = 0.01, 0.01
Nrr = 256
S_f = Function.loop_gausian(Nrr, f1, f2, c1, c2)
real, imag = Function.idft(S_f)
S = (real + imag) * 2
hmean = 60/60
S = Function.scaling(S, hmean)

sideBySide(S_f, S)

# step 2
theta = Angle()
theta.to_radians()

Alpha = Amplitude()
Beta = Amplitude()

hfactor2, hfactor1 = Function.doubleFactorial(hmean)

Beta.scale_by(hfactor2)

theta.p = theta.p * hfactor2
theta.q = theta.q * hfactor1
theta.s = theta.s * hfactor1
theta.t = theta.t * hfactor2

# Print the properties of Alpha, Beta, and theta objects
print(f"Theta p: {theta.p}, q: {theta.q}, s: {theta.s}, t: {theta.t}")
print(f"Alpha p: {Alpha.p}, q: {Alpha.q}, s: {Alpha.s}, t: {Alpha.t}")
print(f"Beta p: {Beta.p}, q: {Beta.q}, s: {Beta.s}, t: {Beta.t}")