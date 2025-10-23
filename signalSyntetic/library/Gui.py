import matplotlib.pyplot as plt
import numpy as np

def singlePlot(data, title='Plot', xlabel='X-axis', ylabel='Y-axis'):
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def singlePlotWithTime(data, time_axis, title='Plot', xlabel='Time (s)', ylabel='Amplitude'):
    """Plot data with proper time axis"""
    plt.figure(figsize=(12, 6))
    plt.plot(time_axis, data, 'b-', linewidth=1)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    
    # Set reasonable time axis limits and ticks
    plt.xlim(0, max(time_axis))
    
    # Add major and minor ticks for better readability
    major_ticks = np.arange(0, max(time_axis) + 0.5, 0.5)  # Every 0.5 seconds
    minor_ticks = np.arange(0, max(time_axis) + 0.1, 0.1)  # Every 0.1 seconds
    
    plt.xticks(major_ticks)
    plt.gca().set_xticks(minor_ticks, minor=True)
    plt.gca().grid(which='minor', alpha=0.2)
    plt.gca().grid(which='major', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

def sideBySide(one, two):
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(one)
    plt.title('S_f')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(two)
    plt.title('S')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    
def plot4Row(one, two, three, four):
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 2, 1)
    plt.plot(one)
    plt.title('Plot 1')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(two)
    plt.title('Plot 2')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(three)
    plt.title('Plot 3')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(four)
    plt.title('Plot 4')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def combine2Plot(one, two):
    plt.figure(figsize=(12, 8))
    
    plt.plot(one, label='Plot 1')
    plt.plot(two, label='Plot 2')
    
    plt.title('Combined Plot')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

