import matplotlib.pyplot as plt
import numpy

fig, ax = plt.subplots()
ax.plot(100 * numpy.random.randn(500), 100 * numpy.random.randn(500), 'o')
ax.set_title('Simple Scatter')

plt.show()
