import numpy
import matplotlib.pyplot as plt

N = 20
theta = numpy.linspace(0.0, 2 * numpy.pi, N, endpoint=False)
radii = 10 * numpy.random.rand(N)
width = numpy.pi / 4 * numpy.random.rand(N)

ax = plt.subplot(111, projection='polar')
bars = ax.bar(theta, radii, width=width, bottom=0.0)  # theta radii width -> left

for r, bar in zip(radii, bars):
	bar.set_facecolor(plt.cm.viridis(r / 10.))
	bar.set_alpha(0.5)

plt.show()
