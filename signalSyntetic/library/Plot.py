import matplotlib.pyplot as plt
import numpy as np

def singlePlot(time_or_data, data=None, title="", xlabel="", ylabel="", mode=None, interactive=True):
    """
    Flexible plot function that works with both Streamlit and regular matplotlib
    
    Args:
        time_or_data: If data is None, this is treated as data. Otherwise, this is the time axis.
        data: The y-axis data (optional)
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        mode: 'streamlit' for Streamlit display, None for regular matplotlib
        interactive: Enable zoom and pan functionality
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
            # Streamlit has built-in zoom with plotly
            if interactive:
                import plotly.graph_objects as go
                fig_plotly = go.Figure()
                fig_plotly.add_trace(go.Scatter(x=list(x_axis), y=list(plot_data), 
                                              mode='lines', name='Signal',
                                              line=dict(color='blue', width=1)))
                fig_plotly.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    showlegend=False,
                    width=800,
                    height=400
                )
                st.plotly_chart(fig_plotly, use_container_width=True)
                plt.close(fig)  # Close matplotlib figure
                return
            else:
                st.pyplot(fig)
        except ImportError as e:
            print(f"Streamlit or Plotly not available: {e}, falling back to matplotlib")
            if interactive:
                # Enable matplotlib zoom/pan toolbar
                plt.subplots_adjust(bottom=0.15)  # Make room for toolbar
            plt.show()
    else:
        if interactive:
            # Enable matplotlib zoom/pan toolbar
            plt.subplots_adjust(bottom=0.15)  # Make room for toolbar
        plt.show()
    
    plt.close(fig)  # Clean up memory

def singlePlotWithTime(time_axis, data, title='Plot', xlabel='Time (s)', ylabel='Amplitude', mode=None, interactive=True):
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
            # Use plotly for interactive zoom in streamlit
            if interactive:
                import plotly.graph_objects as go
                fig_plotly = go.Figure()
                fig_plotly.add_trace(go.Scatter(x=list(time_axis), y=list(data), 
                                              mode='lines', name='Signal',
                                              line=dict(color='blue', width=1)))
                fig_plotly.update_layout(
                    title=title,
                    xaxis_title=xlabel,
                    yaxis_title=ylabel,
                    showlegend=False,
                    width=1000,
                    height=500,
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
                )
                st.plotly_chart(fig_plotly, use_container_width=True)
                plt.close(fig)  # Close matplotlib figure
                return
            else:
                st.pyplot(fig)
        except ImportError as e:
            print(f"Streamlit or Plotly not available: {e}, falling back to matplotlib")
            if interactive:
                plt.subplots_adjust(bottom=0.15)  # Make room for toolbar
            plt.show()
    else:
        if interactive:
            plt.subplots_adjust(bottom=0.15)  # Make room for toolbar
        plt.show()
    
    plt.close(fig)  # Clean up memory

def sideBySide(one, two, mode=None, interactive=True):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(one)
    ax1.set_title('S_f')
    ax1.grid(True)

    ax2.plot(two)
    ax2.set_title('S')
    ax2.grid(True)

    if interactive:
        plt.subplots_adjust(bottom=0.15)  # Make room for toolbar
    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            if interactive:
                import plotly.graph_objects as go
                from plotly.subplots import make_subplots
                
                fig_plotly = make_subplots(rows=1, cols=2, subplot_titles=('S_f', 'S'))
                fig_plotly.add_trace(go.Scatter(y=list(one), mode='lines', name='S_f'), row=1, col=1)
                fig_plotly.add_trace(go.Scatter(y=list(two), mode='lines', name='S'), row=1, col=2)
                fig_plotly.update_layout(showlegend=False, width=1000, height=400)
                st.plotly_chart(fig_plotly, use_container_width=True)
                plt.close(fig)
                return
            else:
                st.pyplot(fig)
        except ImportError:
            print("Streamlit or Plotly not available, falling back to matplotlib")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)

def plot4Row(one, two, three, four, mode=None, interactive=True):
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

    if interactive:
        plt.subplots_adjust(bottom=0.1)
    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            if interactive:
                import plotly.graph_objects as go
                from plotly.subplots import make_subplots
                
                fig_plotly = make_subplots(rows=2, cols=2, 
                                         subplot_titles=('Plot 1', 'Plot 2', 'Plot 3', 'Plot 4'))
                fig_plotly.add_trace(go.Scatter(y=list(one), mode='lines', name='Plot 1'), row=1, col=1)
                fig_plotly.add_trace(go.Scatter(y=list(two), mode='lines', name='Plot 2'), row=1, col=2)
                fig_plotly.add_trace(go.Scatter(y=list(three), mode='lines', name='Plot 3'), row=2, col=1)
                fig_plotly.add_trace(go.Scatter(y=list(four), mode='lines', name='Plot 4'), row=2, col=2)
                fig_plotly.update_layout(showlegend=False, width=1000, height=600)
                st.plotly_chart(fig_plotly, use_container_width=True)
                plt.close(fig)
                return
            else:
                st.pyplot(fig)
        except ImportError:
            print("Streamlit or Plotly not available, falling back to matplotlib")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)

def combine2Plot(one, two, label='Plot 1', label2='Plot 2', mode=None, interactive=True):
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(one, label=label)
    ax.plot(two, label=label2)

    ax.set_title('Combined Plot')
    ax.legend()
    ax.grid(True)
    
    if interactive:
        plt.subplots_adjust(bottom=0.15)
    plt.tight_layout()
    
    if mode == 'streamlit':
        try:
            import streamlit as st
            if interactive:
                import plotly.graph_objects as go
                
                fig_plotly = go.Figure()
                fig_plotly.add_trace(go.Scatter(y=list(one), mode='lines', name=label))
                fig_plotly.add_trace(go.Scatter(y=list(two), mode='lines', name=label2))
                fig_plotly.update_layout(
                    title='Combined Plot',
                    width=1000,
                    height=500,
                    showlegend=True
                )
                st.plotly_chart(fig_plotly, use_container_width=True)
                plt.close(fig)
                return
            else:
                st.pyplot(fig)
        except ImportError:
            print("Streamlit or Plotly not available, falling back to matplotlib")
            plt.show()
    else:
        plt.show()
    
    plt.close(fig)
    return ax