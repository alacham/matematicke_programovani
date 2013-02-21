import pylab as plt
import numpy as np

def demo_hist(n):
  values = np.random.randn(n)
  plt.hist(values)
  plt.show()


def demo_lines():
  x = np.linspace(-6, 6, 40)
  plt.plot(x, x**3 -x**2 - 4*x + 2)
  plt.show()

demo_hist(10)

demo_lines()
