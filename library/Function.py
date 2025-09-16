from math import exp, sqrt
import numpy
import random

class Function:
    def loop_gausian(Nrr, f1, f2, c1, c2):
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

    def idft(S):
        real = [0 for _ in range(len(S))]
        imag = [0 for _ in range(len(S))]
        N = len(S)
        for n in range(N):
            for k in range(N):
                real[n] += S[k] * numpy.cos(2 * numpy.pi * random.random())
                imag[n] += S[k] * numpy.sin(2 * numpy.pi * random.random())
            real[n] /= N
            imag[n] /= N
        return real, imag

    def scaling(s):
        for i in range(len(s)):
            s[i] = s[i] + 1
        return s