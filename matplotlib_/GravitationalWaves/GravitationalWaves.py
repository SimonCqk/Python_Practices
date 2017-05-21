#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
E.g of drawing Gravitational Waves with SciPy/numpy/matplotlib
@author CQK. 2017.05.21 referenced from `mooc`
"""
import matplotlib.pyplot as plt
import numpy
from scipy.io import wavfile

# Generate time series from docs
rate_h, hstrain = wavfile.read(r"matplotlib_/H1_Strain.wav", 'rb')
rate_l, lstrain = wavfile.read(r"matplotlib_/L1_Strain.wav", 'rb')
reftime, ref_H1 = numpy.genfromtxt("matplotlib_/GW150914_4_NR_waveform_template.txt").transpose()
# Read the strain sequence
htime_interval = 1 / rate_h
ltime_interval = 1 / rate_l

htime_len = hstrain.shape[0] / rate_h
htime = numpy.arange(-htime_len / 2, htime_len / 2, htime_interval)
ltime_len = lstrain.shape[0] / rate_l
ltime = numpy.arange(-ltime_len / 2, ltime_len / 2, ltime_interval)
# draw the H1 Strain
fig = plt.figure(figsize=(12, 6))

plth = fig.add_subplot(221)
plth.plot(htime, hstrain, 'r')
plth.set_xlabel('Time (seconds)')
plth.set_ylabel('H1 Strain')
plth.set_title('H1 Strain')
# draw the L1 Strain
pltl = fig.add_subplot(222)
pltl.plot(ltime, lstrain, 'b')
pltl.set_xlabel('Time (seconds)')
pltl.set_ylabel('L1 Strain')
pltl.set_title('L1 Strain')
# draw the Template
pltref = fig.add_subplot(212)
pltref.plot(reftime, ref_H1)
pltref.set_xlabel('Time (seconds)')
pltref.set_ylabel('Template Strain')
pltref.set_title('Template')
fig.tight_layout()

fig.tight_layout()
# show and save img
plt.savefig("Gravitational_Waves_Original.png", dpi=500)
plt.show()
plt.close(fig)
