from math import exp, sqrt
import numpy
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
            S1[i] = magSf * exp(-((f - f1) ** 2 / (2 * c1 ** 2))) / sqrt(2 * numpy.pi * c1 ** 2)
            S2[i] = 2 * magSf * exp(-((f - f2) ** 2 / (2 * c2 ** 2))) / sqrt(2 * numpy.pi * c2 ** 2)
            S[i] = (S1[i] + S2[i])
            
        for i in range(int(Nrr / 2), Nrr):
            S[i] = S[Nrr - i]

        for i in range(Nrr):
            S[i] = sqrt(S[i]) 
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

    def scaling(s, hmean):
        for i in range(len(s)):
            s[i] = s[i] + (hmean / 60)
        return s
    
    def doubleFactorial(hr):
        if hr <= 0:
            return 1
        else:
            hrfactorial = sqrt(hr/60)
            return sqrt(hrfactorial), hrfactorial