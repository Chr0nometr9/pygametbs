from matplotlib import pyplot as plt
import numpy as np
def f(x):
    return (x+1)*(x-2)*(x-4)*0.1
x = np.linspace(-6, 6, 100)
y = f(x)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.xlim(-2, 6)
plt.ylim(-5, 5)
plt.plot(x, y, color='green')
plt.show()