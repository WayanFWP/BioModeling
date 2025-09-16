import matplotlib.pyplot as plt

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