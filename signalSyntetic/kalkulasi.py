from library.Function import *
from library.Plot import *
from library.Variable import *

# step 1
f1 = 0.1    # LF component center frequency
f2 = 0.25   # HF component center frequency  
c1 = 0.01   # LF bandwidth
c2 = 0.01   # HF bandwidth
duration = 10# Duration in seconds
hmean = 50  # Mean heart rate (BPM)
hstd = 1    # Heart rate standard deviation (BPM)
fs = 256    # Sampling frequency (Hz)
Nrr = int(duration * fs)   
print(f"Nrr: {Nrr}")

rr_intervals, info = generate(
    f1=0.1, f2=0.25, c1=0.01, c2=0.01,
    duration=duration, hmean=hmean, fs=fs, hstd=hstd
)
SDNN_value = info['SDNN']
RMSSD_value = info['RMSSD']
pNN50_value = info['pNN50']

print(f"SDNN: {SDNN_value:.2f} milisec")
print(f"RMSSD: {RMSSD_value:.2f} seconds")
print(f"pNN50: {pNN50_value:.2f} %")

print(f"Beat per minute (BPM): {60 / np.mean(rr_intervals):.2f}")

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
dt = 1 / fs
result = Function.solveEcgModel(dt, Nrr, {
    'dt': dt,
    'rr_series': rr_intervals,
    'ai': [Alpha.p, Alpha.q, Alpha.r, Alpha.s, Alpha.t],
    'bi': [Beta.p, Beta.q, Beta.r, Beta.s, Beta.t],
    'ti': [theta.p, theta.q, theta.r, theta.s, theta.t]
}) 

time = np.arange(0, len(result)) / fs
singlePlotWithTime(time, result, title='ECG Signal', xlabel='Time', ylabel='Amplitude')