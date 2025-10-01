import matplotlib.pyplot as plt

def singlePlot(data, title='Plot', xlabel='X-axis', ylabel='Y-axis'):
    plt.figure(figsize=(10, 5))
    plt.plot(data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
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

