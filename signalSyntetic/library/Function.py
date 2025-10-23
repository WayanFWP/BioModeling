import numpy as np
import random

class Function:
    @staticmethod
    def gaussianLoop(Nrr, f1, f2, c1, c2):
        magSf = 1.7 / Nrr
        
        # Create frequency array
        i_vals = np.arange(1, Nrr//2)
        f = i_vals / Nrr
        
        S1 = magSf * np.exp(-((f - f1) ** 2) / (2 * c1 ** 2)) / np.sqrt(2 * np.pi * c1 ** 2)
        S2 = 2 * magSf * np.exp(-((f - f2) ** 2) / (2 * c2 ** 2)) / np.sqrt(2 * np.pi * c2 ** 2)
        S_total = S1 + S2
        
        S = np.zeros(Nrr)
        S[1:Nrr//2] = S_total
        S[Nrr//2+1:] = S[1:Nrr//2][::-1]
        
        return np.sqrt(S), np.sqrt(S_total)
    
    @staticmethod
    def randomPhase(S, N):
        real = np.zeros(N)
        imag = np.zeros(N)
        
        for n in range(N):
            phase = 2 * np.pi * random.random()
            real[n] = S[n] * np.cos(phase)
            imag[n] = S[n] * np.sin(phase)

        return real.tolist(), imag.tolist()

    @staticmethod
    def idft(re, im, N):
        real = np.zeros(N)
        imag = np.zeros(N)
        
        # for n in range(N):
        #     for k in range(N):
        #         angle = 2 * np.pi * k * n / N
        #         real[n] += re[k] * np.cos(angle) - im[k] * np.sin(angle)
        #         imag[n] += re[k] * np.sin(angle) + im[k] * np.cos(angle)
        #     real[n] /= N
        #     imag[n] /= N
        
        # return real, imag
        result = np.fft.ifft(np.array(re) + 1j * np.array(im)) * N
        return result.real.tolist(), result.imag.tolist()
    
    @staticmethod
    def derivative(t, x, y, z, params):
        dt = params['dt']
        rr_series = params['rr_series']
        ai = params['ai']
        bi = params['bi'] 
        ti = params['ti']
        
        omega = Utility.angfreq(t, dt, rr_series)
        
        # alpha calculation based on paper
        alpha = 1.0 - np.sqrt(x**2 + y**2)
        
        dx = alpha * x - omega * y
        dy = alpha * y + omega * x

        theta = np.arctan2(y, x)

        z_sum = 0
        for i in range(len(ai)):
            delta_theta = (theta - ti[i]) % (2 * np.pi)
            if delta_theta > np.pi:
                delta_theta -= 2 * np.pi
            
            z_sum += ai[i] * delta_theta * np.exp(-0.5 * (delta_theta**2) / (bi[i]**2))
        
        # Respiratory baseline wandering
        f_resp = 0.3  # Respiratory frequency (Hz)
        z_baseline = 0.005 * np.sin(2 * np.pi * f_resp * t)

        dz = -z_sum - (z - z_baseline)
        
        return dx, dy, dz

    @staticmethod
    def solveEcgModel(dt, Nrr, params):
        """Solve the ECG dynamical model using Runge Kutta order 4"""
        # Initial conditions
        x = [1.0, 0.0, 0.04]  # Start on the limit cycle
        
        # Storage arrays
        xt = []
        yt = []
        zt = []
        
        t = 0.0
        
        for i in range(Nrr):
            xt.append(x[0])
            yt.append(x[1])
            zt.append(x[2])
            
            # Runge-Kutta 4th order
            k1 = Function.derivative(t, x[0], x[1], x[2], params)
            
            k2 = Function.derivative(
                t + dt/2, 
                x[0] + dt*k1[0]/2, 
                x[1] + dt*k1[1]/2, 
                x[2] + dt*k1[2]/2, 
                params
            )
            
            k3 = Function.derivative(
                t + dt/2,
                x[0] + dt*k2[0]/2,
                x[1] + dt*k2[1]/2,
                x[2] + dt*k2[2]/2,
                params
            )
            
            k4 = Function.derivative(
                t + dt,
                x[0] + dt*k3[0],
                x[1] + dt*k3[1], 
                x[2] + dt*k3[2],
                params
            )
            
            # Update state variables
            x[0] += dt * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6
            x[1] += dt * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6
            x[2] += dt * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2]) / 6
            
            t += dt
        
        return zt


class Utility:
    @staticmethod
    def scaling(s, hmean):
        """Scale RR intervals to have correct mean heart rate"""
        s = np.array(s)
        s_mean = np.mean(s)
        
        # Convert to RR intervals in seconds
        rr_intervals = (s - s_mean) * 0.1 + (60.0 / hmean)  # Base RR + variation
        
        # Ensure positive values
        rr_intervals = np.maximum(rr_intervals, 0.4)  # Minimum RR = 0.4s (150 BPM max)
        
        return rr_intervals.tolist()
    
    @staticmethod
    def doubleFactorial(hr):
        if hr <= 0:
            return 1.0, 1.0
        
        # Scaling based on heart rate
        hr_factor = np.sqrt(hr / 60.0)
        return hr_factor, hr_factor**2
    
    @staticmethod
    def normalize(data):
        """Normalize data to [0, 1] range"""
        data = np.array(data)
        min_val = np.min(data)
        max_val = np.max(data)
        
        if max_val - min_val == 0:
            return np.ones_like(data).tolist()
        
        normalized = (data - min_val) / (max_val - min_val)
        return normalized.tolist()

    @staticmethod
    def angfreq(t, dt, rr_series):
        """Calculate instantaneous angular frequency from RR intervals"""
        # Get current index in RR series
        idx = int(t / dt) % len(rr_series)
        
        # Current RR interval
        rr_current = rr_series[idx]
        
        # Convert RR interval to angular frequency
        # omega = 2*pi / RR_interval
        omega = 2.0 * np.pi / rr_current
        
        return omega
    
    @staticmethod
    def SDNN(rr_intervals):
        """Calculate SDNN from RR intervals (input in seconds, output in ms)"""
        rr_array = np.array(rr_intervals) * 1000.0  # Convert seconds to ms first
        sdnn = np.std(rr_array)  # Calculate std in ms
        return sdnn

    @staticmethod
    def RMSSD(rr_intervals):
        """Calculate RMSSD from RR intervals (input in seconds, output in ms)"""
        rr_array = np.array(rr_intervals) * 1000.0  # Convert seconds to ms first
        diff = np.diff(rr_array)
        rmssd = np.sqrt(np.mean(diff**2))  # Calculate RMSSD in ms
        return rmssd

    @staticmethod
    def pNN50(rr_intervals):
        """Calculate pNN50 from RR intervals (input in seconds, output in %)"""
        rr_array = np.array(rr_intervals) * 1000.0  # Convert seconds to ms first
        diff = np.diff(rr_array)
        pnn50 = np.sum(np.abs(diff) > 50.0) / len(diff) * 100.0  # 50ms threshold
        return pnn50
    
    
def generate(f1, f2, c1, c2, duration, hmean, fs):  # Add verbose flag
    """Optimized generate function"""
    Nrr = int(duration * fs)
    print(f"Nrr: {Nrr}")
    
    # Pre-compute base spectrum once
    Sw_base = Function.gaussianLoop(Nrr, f1, f2, c1, c2)

    # Use optimized functions
    real_0, imag_0 = Function.randomPhase(Sw_base, Nrr)
    real, imag = Function.idft(real_0, imag_0, Nrr)
    
    # Combine operations
    S = (real + imag) * 2

    rr_intervals = Utility.scaling(S, hmean)

    metrics = {
        'SDNN': Utility.SDNN(rr_intervals),
        'RMSSD': Utility.RMSSD(rr_intervals), 
        'pNN50': Utility.pNN50(rr_intervals)
    }
    return rr_intervals, metrics
