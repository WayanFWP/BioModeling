import math
import random

class Function:
    def gaussianLoop(Nrr, f1, f2, c1, c2):
        S = [0 for _ in range(Nrr)]
        S1 = [0 for _ in range(Nrr)]
        S2 = [0 for _ in range(Nrr)]
        magSf = 1.7 / Nrr
        
        for i in range(1, int(Nrr / 2)):
            f = i * (1 / Nrr)
            S1[i] = magSf * math.exp(-((f - f1) ** 2 / (2 * c1 ** 2))) / math.sqrt(2 * math.pi * c1 ** 2)
            S2[i] = 2 * magSf * math.exp(-((f - f2) ** 2 / (2 * c2 ** 2))) / math.sqrt(2 * math.pi * c2 ** 2)
            S[i] = (S1[i] + S2[i])
            
        for i in range(int(Nrr / 2), Nrr):
            S[i] = S[Nrr - i]

        for i in range(Nrr):
            S[i] = math.sqrt(S[i]) 
        return S
    
    def randomPhase(S, N):
        real = [0 for _ in range(N)]
        imag = [0 for _ in range(N)]
        for n in range(N):
            real[n] = S[n] * math.cos(2 * math.pi * random.random())
            imag[n] = S[n] * math.sin(2 * math.pi * random.random())
        return real, imag

    def idft(re, im, N):
        real = [0 for _ in range(len(re))]
        imag = [0 for _ in range(len(im))]
        for n in range(N):
            for k in range(N):
                real[n] += re[k] * math.cos(2 * math.pi * k * n / N)
                imag[n] += im[k] * math.sin(2 * math.pi * k * n / N)
            real[n] /= N
            imag[n] /= N
        return real, imag
    
    @staticmethod
    def derivative(t, x, y, z, params):
        dt, rr_series = params['dt'], params['rr_series']
        ai, bi, ti = params['ai'], params['bi'], params['ti']

        omega = Utility.angfreq(t, dt, rr_series)

        # alpha calculation based on paper
        alpha = 1.0 - math.sqrt(x**2 + y**2)

        dx = alpha * x - omega * y
        dy = alpha * y + omega * x

        theta = math.atan2(y, x)
        z_sum = 0
        for i in range(len(ai)):
            # delta_theta = (theta - theta_i) mod 2*pi
            delta_theta = ((theta - ti[i] + math.pi) % (2 * math.pi)) - math.pi
            z_sum += ai[i] * delta_theta * math.exp(-0.5 * delta_theta**2 / bi[i]**2)

        f_resp = 0.3  # Frequency of the respiratory component in Hz
        z_base = 0.005 * math.sin(2 * math.pi * f_resp * t)

        dz = -z_sum - (z - z_base)

        return dx, dy, dz

    @staticmethod
    def solveEcgModel(dt, Nrr, params):
        x = [0.1, 0.0, 0.04]  # Initial conditions: x, y, z
        xt = [0 for _ in range(Nrr)]
        yt = [0 for _ in range(Nrr)]
        zt = [0 for _ in range(Nrr)]
        t = 0.0
        
        for i in range(Nrr):
            xt[i] = x[0]
            yt[i] = x[1]
            zt[i] = x[2]
            
            # k1
            k1 = Function.derivative(t, x[0], x[1], x[2], params)
            k1x, k1y, k1z = k1[0], k1[1], k1[2]
            
            # k2
            k2 = Function.derivative(t + dt / 2, x[0] + dt / 2 * k1x, x[1] + dt / 2 * k1y, x[2] + dt / 2 * k1z, params)
            k2x, k2y, k2z = k2[0], k2[1], k2[2]
            
            # k3
            k3 = Function.derivative(t + dt / 2, x[0] + dt / 2 * k2x, x[1] + dt / 2 * k2y, x[2] + dt / 2 * k2z, params)
            k3x, k3y, k3z = k3[0], k3[1], k3[2]
            
            # k4
            k4 = Function.derivative(t + dt, x[0] + dt * k3x, x[1] + dt * k3y, x[2] + dt * k3z, params)
            k4x, k4y, k4z = k4[0], k4[1], k4[2]
            
            # Update x, y, z using RK4
            x[0] += dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
            x[1] += dt / 6 * (k1y + 2 * k2y + 2 * k3y + k4y)
            x[2] += dt / 6 * (k1z + 2 * k2z + 2 * k3z + k4z)
            
            t += dt
        
        return zt 
        

class Utility:
    @staticmethod
    def scaling(s, hmean):
        for i in range(len(s)):
            s[i] = s[i] + (60 / hmean)
        return s
    
    @staticmethod
    def doubleFactorial(hr):
        if hr <= 0:
            return 1
        else:
            hrfactorial = math.sqrt(hr/60)
            return math.sqrt(hrfactorial), hrfactorial
        
    @staticmethod
    def normalize(data):
        min_val = min(data)
        max_val = max(data)
        # Handle case where all values are the same (avoid division by zero)
        if max_val - min_val == 0:
            return [1.0] * len(data)  # Return array of ones if all values are the same
        return [(x - min_val) / (max_val - min_val) for x in data]

    @staticmethod
    def angfreq(t, dt, rr_series):
        idx = min(len(rr_series) - 1, max(0, int(math.floor(t / dt))))
        normalized_rr = Utility.normalize(rr_series)
        # Add a small epsilon to avoid division by zero
        rr_value = max(0.01, normalized_rr[idx])
        return 2 * math.pi / rr_value