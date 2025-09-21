from library.Function import *
from library.Gui import *
from library.Variable import *

# step 1
f1 = 0.1
f2 = 0.25
c1, c2 = 0.01, 0.01
Nrr = 2560
# Nrr = 1258
hmean = 60
Sw = Function.gaussianLoop(Nrr, f1, f2, c1, c2)
real_0, imag_0 = Function.randomPhase(Sw,Nrr)
real, imag = Function.idft(real_0, imag_0, Nrr)
S = (real + imag) * 2
S = Utility.scaling(S, hmean)

plotTwo(real_0, imag_0)
sideBySide(Sw, S)

# step 2
theta = Angle(p=60, q=-15, r=0, s=15, t=90)  # Angles in degrees
theta.to_radians()

Alpha = Amplitude(p=1.2, q=-5.0, r=30.0, s=-7.5, t=0.75)
Beta = Amplitude(p=0.25, q=0.1, r=0.1, s=0.1, t=0.4)

hfactor2, hfactor1 = Utility.doubleFactorial(hmean)

Beta.scale_by(hfactor2)

theta.p = theta.p * hfactor2
theta.q = theta.q * hfactor1
theta.s = theta.s * hfactor1
theta.t = theta.t * hfactor2

# Print the properties of Alpha, Beta, and theta objects
print(f"Theta p: {theta.p}, q: {theta.q}, s: {theta.s}, t: {theta.t}")
print(f"Alpha p: {Alpha.p}, q: {Alpha.q}, s: {Alpha.s}, t: {Alpha.t}")
print(f"Beta p: {Beta.p}, q: {Beta.q}, s: {Beta.s}, t: {Beta.t}")

# step 3
result = Function.solveEcgModel(0.01, Nrr, {
    'dt': 0.01,
    'rr_series': [1.0] * Nrr,
    'ai': [Alpha.p, Alpha.q, Alpha.r, Alpha.s, Alpha.t],
    'bi': [Beta.p, Beta.q, Beta.r, Beta.s, Beta.t],
    'ti': [theta.p, theta.q, theta.r, theta.s, theta.t]
}) 

singlePlot(result, title='ECG Signal', xlabel='Time', ylabel='Amplitude')
