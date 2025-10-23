import matplotlib.pyplot as plt
import numpy as np

def singlePlot(time_or_data, data=None, title="", xlabel="", ylabel="", mode=None):
    """
    Flexible plot function that works with both Streamlit and regular matplotlib
    
    Args:
        time_or_data: If data is None, this is treated as data. Otherwise, this is the time axis.
        data: The y-axis data (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        mode: 'streamlit' for Streamlit display, None for regular matplotlib
    """
    if data is None:
        plot_data = time_or_data
        x_axis = range(len(plot_data))
    else:
        x_axis = time_or_data
        plot_data = data
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_axis, plot_data, 'b-', linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            st.pyplot(fig)
        except ImportError:
            print("Streamlit not available, falling back to regular display")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)  # Clean up memory

def singlePlotWithTime(time_axis, data, title='Plot', xlabel='Time (s)', ylabel='Amplitude', mode=None):
    """Plot data with proper time axis and enhanced formatting"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(time_axis, data, 'b-', linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    
    ax.set_xlim(0, max(time_axis))
    
    major_ticks = np.arange(0, max(time_axis) + 0.5, 0.5)  # Every 0.5 seconds
    minor_ticks = np.arange(0, max(time_axis) + 0.1, 0.1)  # Every 0.1 seconds
    
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    
    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            st.pyplot(fig)
        except ImportError:
            print("Streamlit not available, falling back to regular display")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)  # Clean up memory

def sideBySide(one, two, mode=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(one)
    ax1.set_title('S_f')
    ax1.grid(True)

    ax2.plot(two)
    ax2.set_title('S')
    ax2.grid(True)

    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            st.pyplot(fig)
        except ImportError:
            print("Streamlit not available, falling back to regular display")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)

def plot4Row(one, two, three, four, mode=None):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

    ax1.plot(one)
    ax1.set_title('Plot 1')
    ax1.grid(True)

    ax2.plot(two)
    ax2.set_title('Plot 2')
    ax2.grid(True)

    ax3.plot(three)
    ax3.set_title('Plot 3')
    ax3.grid(True)

    ax4.plot(four)
    ax4.set_title('Plot 4')
    ax4.grid(True)

    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            st.pyplot(fig)
        except ImportError:
            print("Streamlit not available, falling back to regular display")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)

def combine2Plot(one, two, mode=None):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(one, label='Plot 1')
    ax.plot(two, label='Plot 2')
    
    ax.set_title('Combined Plot')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            st.pyplot(fig)
        except ImportError:
            print("Streamlit not available, falling back to regular display")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)