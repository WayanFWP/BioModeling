# BioMod Signal Synthetic

A comprehensive toolkit for generating synthetic ECG signals and RR intervals with Heart Rate Variability (HRV) analysis. This project provides multiple interfaces including PyQt GUI, Streamlit web app, and manual calculation scripts.

## 🔬 Project Overview

BioMod Signal Synthetic generates realistic ECG signals by:
1. Creating synthetic RR intervals using Gaussian power spectrum modeling
2. Calculating HRV metrics (SDNN, RMSSD, pNN50)
3. Generating ECG waveforms using a dynamical system model
4. Providing interactive visualization and analysis tools

## 📁 Project Structure

```
BioMod/signalSyntetic/
├── README.md
├── requirements.txt
├── app.py                      # Streamlit web application
├── kalkulasi.py               # Manual calculation script
├── library/
│   ├── Function.py            # Core signal processing functions
│   ├── Variable.py            # Data classes for angles and amplitudes
│   └── Plot.py                # Plotting utilities
└── ui/
    ├── gui.py                 # PyQt desktop application
    ├── design.ui              # UI design file
```

## 🚀 Features

### Core Capabilities
- **RR Interval Generation**: Creates realistic heart rate variability patterns
- **ECG Signal Synthesis**: Generates complete ECG waveforms with P, Q, R, S, T waves
- **HRV Analysis**: Calculates standard HRV metrics
- **Multiple Interfaces**: Desktop GUI, web app, and command-line tools

### Signal Processing
- Gaussian power spectrum modeling for LF/HF components
- Random phase generation with inverse DFT
- Dynamical system-based ECG modeling
- Configurable heart rate parameters

### Visualization
- Interactive plots with zoom functionality
- Real-time parameter adjustment
- Multiple plot types (time series, spectra, phase plots)

## 📋 Requirements

### System Requirements
- Python 3.7+
- Linux/Windows/macOS

### Python Dependencies
```bash
pip install -r requirements.txt
```

**Core packages:**
- `numpy` - Numerical computations
- `matplotlib` - Plotting and visualization
- `scipy` - Scientific computing

**GUI packages:**
- `PyQt5` - Desktop GUI framework
- `streamlit` - Web application framework
- `plotly` - Interactive web plots

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd BioMod/signalSyntetic
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python kalkulasi.py
```

## 🖥️ Usage

### 1. PyQt Desktop GUI

**Launch the desktop application:**
```bash
cd ui
python gui.py
```

**Features:**
- Real-time parameter adjustment
- Interactive plots with mouse wheel zoom
- Double-click to reset zoom
- Generate button for signal creation
- Comprehensive HRV metrics display

**Controls:**
- **Duration**: Signal length (1-600 seconds)
- **HR Mean**: Average heart rate (30-180 BPM)
- **HR Std**: Heart rate variability (0-20 BPM)
- **Sampling**: Sampling frequency (128-1024 Hz)

### 2. Streamlit Web Application

**Launch the web app:**
```bash
streamlit run app.py
```

**Features:**
- Web-based interface accessible via browser
- Automatic signal generation on parameter change
- Interactive Plotly charts with zoom/pan
- Sidebar parameter controls
- Responsive layout

**Access:** Open browser to `http://localhost:8501`

### 3. Manual Calculation

**Run the calculation script:**
```bash
python kalkulasi.py
```

**Features:**
- Direct parameter control in code
- Step-by-step signal generation
- Matplotlib plots with toolbar
- Educational debugging output

## 🔧 Configuration

### Default Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Duration | 10 s | 1-600 s | Signal length |
| HR Mean | 60 BPM | 30-180 BPM | Average heart rate |
| HR Std | 1.0 BPM | 0-20 BPM | Heart rate variability |
| Sampling | 256 Hz | 128-1024 Hz | Sampling frequency |

### Fixed HRV Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| f1 | 0.1 Hz | LF center frequency |
| f2 | 0.25 Hz | HF center frequency |
| c1 | 0.01 Hz | LF bandwidth |
| c2 | 0.01 Hz | HF bandwidth |

### ECG Model Parameters

| Component | Angle (°) | Amplitude | Width |
|-----------|-----------|-----------|-------|
| P wave | -60 | 1.2 | 0.25 |
| Q wave | -15 | -5.0 | 0.1 |
| R wave | 0 | 30.0 | 0.1 |
| S wave | 15 | -7.5 | 0.1 |
| T wave | 90 | 0.75 | 0.4 |

## 📊 Output Metrics

### HRV Metrics
- **SDNN**: Standard deviation of RR intervals (ms)
- **RMSSD**: Root mean square of successive differences (ms)
- **pNN50**: Percentage of adjacent RR intervals differing by >50ms (%)
- **BPM**: Heart rate in beats per minute

### Generated Plots
1. **Total Power Spectrum**: Combined LF/HF frequency components
2. **RSA Mayer**: Individual frequency components
3. **Random Phase Components**: Real and imaginary parts
4. **RR Intervals**: Time series of beat-to-beat intervals
5. **ECG Signal**: Complete synthetic electrocardiogram

## 🔬 Algorithm Overview

### Step 1: RR Interval Generation
```python
# Generate Gaussian power spectrum
Sw, total = Function.gaussianLoop(Nrr, f1, f2, c1, c2)

# Add random phase
real_0, imag_0 = Function.randomPhase(Sw, Nrr)

# Inverse DFT to time domain
real, imag = Function.idft(real_0, imag_0, Nrr)

# Scale to physiological range
rr_intervals = Utility.scaling(S, hmean, hstd)
```

### Step 2: HRV Analysis
```python
# Calculate standard HRV metrics
metrics = {
    'SDNN': Utility.SDNN(rr_intervals),
    'RMSSD': Utility.RMSSD(rr_intervals),
    'pNN50': Utility.pNN50(rr_intervals)
}
```

### Step 3: ECG Generation
```python
# Set up dynamical system parameters
theta = Angle(p=-60, q=-15, r=0, s=15, t=90)
Alpha = Amplitude(p=1.2, q=-5.0, r=30.0, s=-7.5, t=0.75)
Beta = Amplitude(p=0.25, q=0.1, r=0.1, s=0.1, t=0.4)

# Solve differential equation
ecg_signal = Function.solveEcgModel(dt, Nrr, params)
```

## 🎯 Use Cases

### Research Applications
- **HRV Studies**: Generate controlled datasets with known parameters
- **Algorithm Testing**: Benchmark HRV analysis algorithms
- **Signal Processing**: Test filtering and preprocessing methods
- **Machine Learning**: Create training datasets for ECG classification

### Educational Applications
- **Biomedical Engineering**: Demonstrate ECG generation principles
- **Signal Processing**: Teach frequency domain analysis
- **Physiology**: Illustrate heart rate variability concepts
- **Programming**: Example of scientific Python applications

### Clinical Applications
- **Device Testing**: Generate test signals for ECG devices
- **Software Validation**: Verify ECG analysis software
- **Training Data**: Create synthetic datasets for AI models

## 📈 Interactive Features

### PyQt GUI
- **Mouse Wheel Zoom**: Zoom in/out on any plot
- **Double-Click Reset**: Return to original view
- **Real-time Updates**: Generate signals with current parameters
- **Status Monitoring**: Progress updates during generation

### Streamlit Web App
- **Live Parameter Updates**: Automatic regeneration on changes
- **Plotly Integration**: Interactive web-based plots
- **Responsive Design**: Works on desktop and mobile
- **Shareable Interface**: Easy to deploy and share

## 🐛 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Install missing dependencies
pip install PyQt5 streamlit plotly
```

**GUI Not Loading:**
```bash
# Check UI file path
ls ui/design.ui ui/untitled.ui
```

**Slow Performance:**
```bash
# Reduce duration or sampling frequency
# Duration: < 60 seconds
# Sampling: < 512 Hz for real-time use
```

### Performance Tips
- Use lower sampling frequencies for faster generation
- Reduce duration for quicker testing
- Close matplotlib figures to free memory
- Use threading for GUI responsiveness

## 📚 References

### Scientific Background
- Heart Rate Variability analysis standards
- ECG dynamical system modeling
- Gaussian power spectrum synthesis
- Biomedical signal processing principles

### Technical Implementation
- PyQt5 documentation for GUI development
- Streamlit documentation for web apps
- Matplotlib/Plotly for visualization
- NumPy/SciPy for signal processing


**Version**: 1.0  
**Last Updated**: October 2024  
**Status**: Active Development