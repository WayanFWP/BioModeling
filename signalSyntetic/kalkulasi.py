from library.Function import *
from library.Gui import *
from library.Variable import *

# step 1
f1 = 0.1    # LF component center frequency
f2 = 0.25   # HF component center frequency  
c1 = 0.01   # LF bandwidth
c2 = 0.01   # HF bandwidth
duration = 5  # Duration in seconds
hmean = 60  # Mean heart rate (BPM)
# fs = 256    # Sampling frequency (Hz)
fs = 512    # Sampling frequency (Hz)
SDNN_value = 0
RMSSD_value = 0
pNN50_value = 0

Nrr = int(duration * fs)   
print(f"Nrr: {Nrr}")
Sw = Function.gaussianLoop(Nrr, f1, f2, c1, c2)
real_0, imag_0 = Function.randomPhase(Sw,Nrr)
real, imag = Function.idft(real_0, imag_0, Nrr)

S = (real + imag) * 2
rr_intervals = Utility.scaling(S, hmean)

SDNN_value = Utility.SDNN(rr_intervals)
RMSSD_value = Utility.RMSSD(rr_intervals)
pNN50_value = Utility.pNN50(rr_intervals)

print(f"Generated RR intervals: {rr_intervals}")
print(f"SDNN: {SDNN_value} seconds")
print(f"RMSSD: {RMSSD_value} seconds")
print(f"pNN50: {pNN50_value:.2f} %")

print(f"Heart rate range: {60/max(rr_intervals):.1f} - {60/min(rr_intervals):.1f} BPM")

# step 2
theta = Angle(p=-60, q=-15, r=0, s=15, t=90)  # Angles in degrees
theta.to_radians()

Alpha = Amplitude(p=1.2, q=-5.0, r=30.0, s=-7.5, t=0.75)
Beta = Amplitude(p=0.25, q=0.1, r=0.1, s=0.1, t=0.4)

hfactor1, hfactor2 = Utility.doubleFactorial(hmean)

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
    'dt': 1/fs,
    'rr_series': rr_intervals,
    'ai': [Alpha.p, Alpha.q, Alpha.r, Alpha.s, Alpha.t],
    'bi': [Beta.p, Beta.q, Beta.r, Beta.s, Beta.t],
    'ti': [theta.p, theta.q, theta.r, theta.s, theta.t]
}) 

time = np.arange(0, len(result)) / fs
singlePlotWithTime(result, time, title='ECG Signal', xlabel='Time', ylabel='Amplitude')