import streamlit as st
from library.Plot import *
from library.Function import *
from library.Variable import *
wider_layout = True
st.set_page_config(layout="wide" if wider_layout else "centered")
class App:
    def __init__(self):
        self.f1 = 0.1
        self.f2 = 0.25
        self.c1 = 0.01
        self.c2 = 0.01
        
        self.duration = st.sidebar.number_input("Duration (seconds)", min_value=1, max_value=600, value=10)
        self.hmean = st.sidebar.number_input("Mean Heart Rate (BPM)", min_value=30, max_value=180, value=60)
        self.hstd = st.sidebar.number_input("Heart Rate Std Dev (BPM)", min_value=0.0, max_value=20.0, value=1.0)
        self.fs = st.sidebar.number_input("Sampling Frequency (Hz)", min_value=128, max_value=1024, value=256)        
        self.Nrr = int(self.duration * self.fs)

        self.initialize_parameters()
        self.generate_ecg_signal()
    
    def initialize_parameters(self):
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric("f1 (LF center freq)", f"{self.f1} Hz")
            st.metric("f2 (HF center freq)", f"{self.f2} Hz")
        with col2:
            st.metric("c1 (LF bandwidth)", f"{self.c1} Hz")
            st.metric("c2 (HF bandwidth)", f"{self.c2} Hz")
        with col3:
            st.metric("Duration", f"{self.duration} seconds")
            st.metric("Sampling Freq", f"{self.fs} Hz")
        with col4:
            st.metric("Mean HR", f"{self.hmean} BPM")
            st.metric("HR Std Dev", f"{self.hstd} BPM")
    
    def generate_rr_intervals(self):
        with st.spinner("Generating RR intervals..."):
            Sw, total = Function.gaussianLoop(self.Nrr, self.f1, self.f2, self.c1, self.c2)
    
            real_0, imag_0 = Function.randomPhase(Sw,self.Nrr)
            real, imag = Function.idft(real_0, imag_0, self.Nrr)
            S = (real + imag) * 2
    
            rr_intervals = Utility.scaling(S, self.hmean, self.hstd)
            # rr_intervals = Utility.scaling(S, self.hmean) 
            
            col1 , col2 = st.columns(2)
            with col1:
                singlePlot(total, title="Total Power Spectrum", xlabel="Sample Index", ylabel="RR Interval (s)", mode='streamlit')
                combine2Plot(real_0, imag_0, label="real", label2="imag", mode='streamlit')
            with col2:
                singlePlot(Sw, title="RSA Mayer", xlabel="Sample Index", ylabel="RR Interval (s)", mode='streamlit')
                singlePlot(rr_intervals, title="Generated RR Intervals", xlabel="Sample Index", ylabel="RR Interval (s)", mode='streamlit')
    
        return rr_intervals
    
    def HRV_metrics(self, rr_intervals):   
        with st.spinner("Calculating HRV metrics..."):    
            info = {
                    'SDNN': Utility.SDNN(rr_intervals),
                    'RMSSD': Utility.RMSSD(rr_intervals),
                    'pNN50': Utility.pNN50(rr_intervals)
                }
            return info
    
    def generate_ecg_signal(self):
        with st.spinner("Generating ECG signal..."):
            rr_intervals = self.generate_rr_intervals()            
            info = self.HRV_metrics(rr_intervals)
        
        theta = Angle(p=-60, q=-15, r=0, s=15, t=90)  # Angles in degrees
        theta.to_radians()

        Alpha = Amplitude(p=1.2, q=-5.0, r=30.0, s=-7.5, t=0.75)
        Beta = Amplitude(p=0.25, q=0.1, r=0.1, s=0.1, t=0.4)

        hfactor1, hfactor2 = Utility.doubleFactorial(self.hmean)

        Beta.scale_by(hfactor2)

        theta.p = theta.p * hfactor2
        theta.q = theta.q * hfactor1
        theta.s = theta.s * hfactor1
        theta.t = theta.t * hfactor2
        dt = 1 / self.fs
        result = Function.solveEcgModel(dt, self.Nrr, {
            'dt': dt,
            'rr_series': rr_intervals,
            'ai': [Alpha.p, Alpha.q, Alpha.r, Alpha.s, Alpha.t],
            'bi': [Beta.p, Beta.q, Beta.r, Beta.s, Beta.t],
            'ti': [theta.p, theta.q, theta.r, theta.s, theta.t]
        }) 
        
        time = np.arange(0, len(result)) / self.fs
        singlePlot(time, result, title='ECG Signal', xlabel='Time', ylabel='Amplitude', mode='streamlit')
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("SDNN", f"{info['SDNN']:.2f} ms")
        with col2:
            st.metric("RMSSD", f"{info['RMSSD']:.2f} ms") 
        with col3:
            st.metric("pNN50", f"{info['pNN50']:.2f} %")
        with col4:
            st.metric("BPM", f"{60 / np.mean(rr_intervals):.2f}")
        
if __name__ == "__main__":
    app = App()