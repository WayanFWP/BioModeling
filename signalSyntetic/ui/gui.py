import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from library.Function import Function, Utility
from library.Variable import Angle, Amplitude

class ZoomOnlyPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
        # Enable interactive mode with tight layout
        self.fig.patch.set_facecolor('white')
        
        # Variables for zoom functionality
        self.zoom_factor = 1.1
        self.original_xlim = None
        self.original_ylim = None
        
        # Connect scroll event for zoom
        self.mpl_connect('scroll_event', self.on_scroll)
        self.mpl_connect('button_press_event', self.on_double_click)
        
    def on_scroll(self, event):
        """Handle mouse wheel zoom"""
        if event.inaxes is None:
            return
            
        ax = event.inaxes
        
        # Get current axis limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Get mouse position
        x_mouse = event.xdata
        y_mouse = event.ydata
        
        if x_mouse is None or y_mouse is None:
            return
        
        # Zoom in or out
        if event.button == 'up':  # Zoom in
            scale = 1 / self.zoom_factor
        elif event.button == 'down':  # Zoom out
            scale = self.zoom_factor
        else:
            return
        
        # Calculate new limits
        x_range = xlim[1] - xlim[0]
        y_range = ylim[1] - ylim[0]
        
        new_x_range = x_range * scale
        new_y_range = y_range * scale
        
        # Center zoom on mouse position
        new_xlim = [x_mouse - new_x_range * (x_mouse - xlim[0]) / x_range,
                   x_mouse + new_x_range * (xlim[1] - x_mouse) / x_range]
        new_ylim = [y_mouse - new_y_range * (y_mouse - ylim[0]) / y_range,
                   y_mouse + new_y_range * (ylim[1] - y_mouse) / y_range]
        
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        self.draw()
        
    def on_double_click(self, event):
        """Reset zoom on double click"""
        if event.dblclick and event.inaxes and self.original_xlim and self.original_ylim:
            ax = event.inaxes
            ax.set_xlim(self.original_xlim)
            ax.set_ylim(self.original_ylim)
            self.draw()
        
    def plot_data(self, data, title="Plot", color='blue', xlabel="Sample Index", ylabel="Amplitude"):
        self.fig.clear()
        
        # Create subplot with margins for axis labels
        ax = self.fig.add_subplot(111)
        
        line, = ax.plot(data, color=color, linewidth=1)
        # Remove title
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=8)
        
        # Store original limits for reset
        self.original_xlim = ax.get_xlim()
        self.original_ylim = ax.get_ylim()
        
        # Adjust margins to show axis labels properly - MORE SPACE FOR LABELS
        self.fig.subplots_adjust(left=0.18, bottom=0.22, right=0.95, top=0.95, wspace=0, hspace=0)
        self.draw()
        
    def plot_xy(self, x_data, y_data, title="Plot", xlabel="X", ylabel="Y", color='blue'):
        self.fig.clear()
        
        # Create subplot with margins for axis labels
        ax = self.fig.add_subplot(111)
        
        line, = ax.plot(x_data, y_data, color=color, linewidth=1)
        # Remove title
        ax.set_xlabel(xlabel, fontsize=10, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=8)
        
        # Store original limits for reset
        self.original_xlim = ax.get_xlim()
        self.original_ylim = ax.get_ylim()
        
        # Adjust margins to show axis labels properly - MORE SPACE FOR LABELS
        self.fig.subplots_adjust(left=0.18, bottom=0.22, right=0.95, top=0.95, wspace=0, hspace=0)
        self.draw()
        
    def plot_combined(self, data1, data2, title="Combined Plot", label1="Real", label2="Imag"):
        self.fig.clear()
        
        # Create subplot with margins for axis labels
        ax = self.fig.add_subplot(111)
        
        line1, = ax.plot(data1, label=label1, linewidth=1, color='blue')
        line2, = ax.plot(data2, label=label2, linewidth=1, color='red')
        
        # Remove title
        ax.set_xlabel("Sample Index", fontsize=10, fontweight='bold')
        ax.set_ylabel("Amplitude", fontsize=10, fontweight='bold')
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=8)
        
        # Store original limits for reset
        self.original_xlim = ax.get_xlim()
        self.original_ylim = ax.get_ylim()
          
        # Adjust margins to show axis labels properly - MORE SPACE FOR LABELS
        self.fig.subplots_adjust(left=0.18, bottom=0.22, right=0.95, top=0.95, wspace=0, hspace=0)
        self.draw()
        
    def plot_empty(self, title="Plot"):
        """Display an empty plot"""
        self.fig.clear()
        
        # Create subplot with margins for axis labels
        ax = self.fig.add_subplot(111)
        
        ax.plot([0, 1], [0, 0], color='lightgray', linewidth=1)
        # Remove title
        ax.set_xlabel("Index", fontsize=10, fontweight='bold')
        ax.set_ylabel("Value", fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=8)
        
        ax.text(0.5, 0.5, 'No data\nScroll to zoom, double-click to reset\nClick Generate to create signal', 
               transform=ax.transAxes, ha='center', va='center',
               fontsize=8, color='gray',
               bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
        
        # Store original limits for reset
        self.original_xlim = ax.get_xlim()
        self.original_ylim = ax.get_ylim()
        
        # Adjust margins to show axis labels properly - MORE SPACE FOR LABELS
        self.fig.subplots_adjust(left=0.18, bottom=0.22, right=0.95, top=0.95, wspace=0, hspace=0)
        self.draw()

class ZoomOnlyPlotWidget(QWidget):
    def __init__(self, parent=None, width=5, height=4):
        super().__init__(parent)
        
        # Create the matplotlib canvas
        self.canvas = ZoomOnlyPlotCanvas(self, width=width, height=height)
        
        # Layout with no margins to fill the border completely
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.canvas)
        
    def plot_data(self, *args, **kwargs):
        return self.canvas.plot_data(*args, **kwargs)
        
    def plot_xy(self, *args, **kwargs):
        return self.canvas.plot_xy(*args, **kwargs)
        
    def plot_combined(self, *args, **kwargs):
        return self.canvas.plot_combined(*args, **kwargs)
        
    def plot_empty(self, *args, **kwargs):
        return self.canvas.plot_empty(*args, **kwargs)

class ECGGenerationThread(QThread):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, params):
        super().__init__()
        self.params = params
    
    def run(self):
        try:
            self.progress.emit("Starting generation...")
            
            # Parameters
            duration = self.params['duration']
            hmean = self.params['hmean']
            hstd = self.params['hstd']
            fs = self.params['fs']
            f1 = 0.1
            f2 = 0.25
            c1 = 0.01
            c2 = 0.01
            
            Nrr = int(duration * fs)
            
            self.progress.emit("Generating Gaussian spectrum...")
            # Generate Gaussian spectrum
            Sw, total = Function.gaussianLoop(Nrr, f1, f2, c1, c2)
            
            self.progress.emit("Generating random phase...")
            # Generate random phase
            real_0, imag_0 = Function.randomPhase(Sw, Nrr)
            
            self.progress.emit("Computing IDFT...")
            # IDFT
            real, imag = Function.idft(real_0, imag_0, Nrr)
            S = (np.array(real) + np.array(imag)) * 2
            
            self.progress.emit("Scaling RR intervals...")
            # Scale to RR intervals
            rr_intervals = Utility.scaling(S, hmean, hstd)
            
            self.progress.emit("Calculating HRV metrics...")
            # Calculate HRV metrics
            metrics = {
                'SDNN': Utility.SDNN(rr_intervals),
                'RMSSD': Utility.RMSSD(rr_intervals),
                'pNN50': Utility.pNN50(rr_intervals),
                'BPM': 60 / np.mean(rr_intervals)
            }
            
            self.progress.emit("Generating ECG signal...")
            # ECG generation
            theta = Angle(p=-60, q=-15, r=0, s=15, t=90)
            theta.to_radians()
            
            Alpha = Amplitude(p=1.2, q=-5.0, r=30.0, s=-7.5, t=0.75)
            Beta = Amplitude(p=0.25, q=0.1, r=0.1, s=0.1, t=0.4)
            
            hfactor1, hfactor2 = Utility.doubleFactorial(hmean)
            Beta.scale_by(hfactor2)
            
            theta.p *= hfactor2
            theta.q *= hfactor1
            theta.s *= hfactor1
            theta.t *= hfactor2
            
            dt = 1 / fs
            ecg_signal = Function.solveEcgModel(dt, Nrr, {
                'dt': dt,
                'rr_series': rr_intervals,
                'ai': [Alpha.p, Alpha.q, Alpha.r, Alpha.s, Alpha.t],
                'bi': [Beta.p, Beta.q, Beta.r, Beta.s, Beta.t],
                'ti': [theta.p, theta.q, theta.r, theta.s, theta.t]
            })
            
            time = np.arange(0, len(ecg_signal)) / fs
            
            result = {
                'total_spectrum': total,
                'sw_spectrum': Sw,
                'real_phase': real_0,
                'imag_phase': imag_0,
                'rr_intervals': rr_intervals,
                'ecg_signal': ecg_signal,
                'time': time,
                'metrics': metrics
            }
            
            self.progress.emit("Generation completed!")
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Load the UI file
        ui_file = os.path.join(os.path.dirname(__file__), 'design.ui')
        uic.loadUi(ui_file, self)
        
        self.setWindowTitle("BioMod Signal Synthetic GUI - Zoom Only")
        
        # Set default values and labels
        self.setup_defaults()
        
        # Setup zoom-only plot widgets
        self.setup_plots()
        
        # Connect the generate button from UI file
        self.pushButton.clicked.connect(self.generate_signal)
        
        # Style the generate button
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
    def setup_defaults(self):
        # Set default values
        self.duration.setText("10")
        self.hrmean.setText("60")
        self.hstd.setText("1.0")
        self.fsampling.setText("256")
        
        # Set labels
        self.label01.setText("Duration (s):")
        self.label02.setText("HR Mean (BPM):")
        self.label03.setText("HR Std (BPM):")
        self.label04.setText("Sampling (Hz):")
        
        # Set initial text
        self.textEdit.setPlainText("BioMod Signal Synthetic GUI - Zoom Only Mode\n\nZoom Features:\n🔍 Mouse Wheel: Zoom in/out centered on cursor\n🔄 Double Click: Reset to original view\n📊 Statistics overlay on plots\n📐 Plots fill entire border area\n\nReady to generate ECG signal.\nAdjust parameters and click 'Generate' button.\n\nDefault Parameters:\n- f1 (LF center): 0.1 Hz\n- f2 (HF center): 0.25 Hz\n- c1 (LF bandwidth): 0.01 Hz\n- c2 (HF bandwidth): 0.01 Hz")
        
    def setup_plots(self):
        # Create zoom-only plot widgets for each plot area - no margins, full border fill
        self.gaussian_widget = ZoomOnlyPlotWidget(self.GausianOutput, width=2.5, height=1.5)
        gaussian_layout = QVBoxLayout(self.GausianOutput)
        gaussian_layout.setContentsMargins(0, 0, 0, 0)
        gaussian_layout.setSpacing(0)
        gaussian_layout.addWidget(self.gaussian_widget)
        
        self.rsa_widget = ZoomOnlyPlotWidget(self.RSAMayer, width=2.5, height=1.5)
        rsa_layout = QVBoxLayout(self.RSAMayer)
        rsa_layout.setContentsMargins(0, 0, 0, 0)
        rsa_layout.setSpacing(0)
        rsa_layout.addWidget(self.rsa_widget)
        
        self.phase_widget = ZoomOnlyPlotWidget(self.RandomPhase, width=2.5, height=1.5)
        phase_layout = QVBoxLayout(self.RandomPhase)
        phase_layout.setContentsMargins(0, 0, 0, 0)
        phase_layout.setSpacing(0)
        phase_layout.addWidget(self.phase_widget)
        
        self.rr_widget = ZoomOnlyPlotWidget(self.RRTachogram, width=2.5, height=1.5)
        rr_layout = QVBoxLayout(self.RRTachogram)
        rr_layout.setContentsMargins(0, 0, 0, 0)
        rr_layout.setSpacing(0)
        rr_layout.addWidget(self.rr_widget)
        
        self.ecg_widget = ZoomOnlyPlotWidget(self.ECG_output, width=5.2, height=1.5)
        ecg_layout = QVBoxLayout(self.ECG_output)
        ecg_layout.setContentsMargins(0, 0, 0, 0)
        ecg_layout.setSpacing(0)
        ecg_layout.addWidget(self.ecg_widget)
        
        # Initialize with empty plots
        self.clear_all_plots()
        
    def clear_all_plots(self):
        """Clear all plots"""
        self.gaussian_widget.plot_empty("Total Power Spectrum")
        self.rsa_widget.plot_empty("RSA Mayer") 
        self.phase_widget.plot_empty("Random Phase Components")
        self.rr_widget.plot_empty("RR Intervals")
        self.ecg_widget.plot_empty("ECG Signal")
            
    def get_parameters(self):
        try:
            duration = float(self.duration.text())
            hmean = float(self.hrmean.text())
            hstd = float(self.hstd.text())
            fs = float(self.fsampling.text())
            
            # Validate parameters
            if duration <= 0 or duration > 600:
                raise ValueError("Duration must be between 1 and 600 seconds")
            if hmean < 30 or hmean > 180:
                raise ValueError("Heart rate must be between 30 and 180 BPM")
            if hstd < 0 or hstd > 20:
                raise ValueError("Heart rate std dev must be between 0 and 20 BPM")
            if fs < 128 or fs > 1024:
                raise ValueError("Sampling frequency must be between 128 and 1024 Hz")
            
            return {
                'duration': duration,
                'hmean': hmean,
                'hstd': hstd,
                'fs': fs
            }
        except ValueError as e:
            return None, str(e)
    
    def generate_signal(self):
        # Get and validate parameters
        result = self.get_parameters()
        if isinstance(result, tuple):  # Error case
            params, error_msg = result
            self.update_status(f"Parameter Error: {error_msg}")
            return
        
        params = result
        
        # Disable button during generation
        self.pushButton.setEnabled(False)
        self.pushButton.setText("Generating...")
        
        # Clear previous results
        self.textEdit.clear()
        self.update_status("Starting ECG generation with zoom-only interactive plots...")
        self.update_status(f"Parameters: Duration={params['duration']}s, HR={params['hmean']}±{params['hstd']}BPM, Fs={params['fs']}Hz")
        
        # Start generation in separate thread
        self.generation_thread = ECGGenerationThread(params)
        self.generation_thread.finished.connect(self.on_generation_finished)
        self.generation_thread.progress.connect(self.update_status)
        self.generation_thread.error.connect(self.on_generation_error)
        self.generation_thread.start()
        
    def update_status(self, message):
        # Update the text edit with status
        current_text = self.textEdit.toPlainText()
        self.textEdit.setPlainText(current_text + message + "\n")
        
        # Scroll to bottom
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.End)
        self.textEdit.setTextCursor(cursor)
        
        # Process events to update UI
        QApplication.processEvents()
        
    def on_generation_error(self, error_msg):
        self.update_status(error_msg)
        
        # Re-enable button
        self.pushButton.setEnabled(True)
        self.pushButton.setText("generate")
        
    def on_generation_finished(self, result):
        try:
            self.update_status("Rendering zoom-only interactive plots...")
            
            # Update all plots with zoom-only matplotlib graphs
            self.gaussian_widget.plot_data(
                result['total_spectrum'], 
                "Total Power Spectrum",
                color='purple',
                xlabel="Frequency Bin",
                ylabel="Power"
            )
            
            self.rsa_widget.plot_data(
                result['sw_spectrum'], 
                "RSA Mayer",
                color='orange',
                xlabel="Frequency Bin", 
                ylabel="Power"
            )
            
            self.phase_widget.plot_combined(
                result['real_phase'], 
                result['imag_phase'],
                "Random Phase Components",
                "Real Part", "Imaginary Part"
            )
            
            self.rr_widget.plot_data(
                result['rr_intervals'], 
                "RR Intervals",
                color='green',
                xlabel="Beat Index",
                ylabel="RR Interval (s)"
            )
            
            self.ecg_widget.plot_xy(
                result['time'], 
                result['ecg_signal'],
                "ECG Signal", 
                "Time (s)", "Amplitude (mV)",
                color='red'
            )
            
            # Update metrics in text area
            metrics = result['metrics']
            params = self.get_parameters()
            
            metrics_text = f"""Generation completed successfully!

=== HRV Metrics ===
SDNN: {metrics['SDNN']:.2f} ms
RMSSD: {metrics['RMSSD']:.2f} ms
pNN50: {metrics['pNN50']:.2f} %
BPM: {metrics['BPM']:.2f}

=== Parameters Used ===
Duration: {params['duration']} s
HR Mean: {params['hmean']} BPM
HR Std: {params['hstd']} BPM
Sampling: {params['fs']} Hz

=== Fixed HRV Parameters ===
f1 (LF center): 0.1 Hz
f2 (HF center): 0.25 Hz
c1 (LF bandwidth): 0.01 Hz
c2 (HF bandwidth): 0.01 Hz

=== Signal Statistics ===
ECG Length: {len(result['ecg_signal'])} samples
Duration: {len(result['ecg_signal'])/params['fs']:.2f} s
RR Count: {len(result['rr_intervals'])} intervals
            """
            
            self.textEdit.setPlainText(metrics_text)
            
        except Exception as e:
            self.update_status(f"Error updating plots: {str(e)}")
        
        # Re-enable button
        self.pushButton.setEnabled(True)
        self.pushButton.setText("generate")

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("BioMod Signal Synthetic - Zoom Only")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()