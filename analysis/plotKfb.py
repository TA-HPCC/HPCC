#!/usr/bin/python

import subprocess
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import ticker
from matplotlib.pyplot import cm
import numpy as np
import pylab
import random
from math import exp,ceil,log
import sys
import os.path
from os import path
import numpy as np

def median(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
    else:
        return sorted_data[mid]
    
    
#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['pdf.use14corefonts'] = True
#matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

fig, ax = plt.subplots(figsize=(10,5))

plt.grid()
plt.gcf().subplots_adjust(bottom=0.15)

fb_file = 'fct_fb50_k_dint.dat'


DINT_1_50_fb = [float(line.split()[2]) for line in open(fb_file).readlines()[0:]]     # web search
DINT_1_95_fb = [float(line.split()[3]) for line in open(fb_file).readlines()[0:]]     # web search
DINT_1_99_fb = [float(line.split()[4]) for line in open(fb_file).readlines()[0:]]     # web search
DINT_2_50_fb = [float(line.split()[5]) for line in open(fb_file).readlines()[0:]]    # web search
DINT_2_95_fb = [float(line.split()[6]) for line in open(fb_file).readlines()[0:]]    # web search
DINT_2_99_fb = [float(line.split()[7]) for line in open(fb_file).readlines()[0:]]    # web search
DINT_3_50_fb = [float(line.split()[8]) for line in open(fb_file).readlines()[0:]]    # web sear>
DINT_3_95_fb = [float(line.split()[9]) for line in open(fb_file).readlines()[0:]]    # web sear>
DINT_3_99_fb = [float(line.split()[10]) for line in open(fb_file).readlines()[0:]]    # web sear>
DINT_4_50_fb = [float(line.split()[11]) for line in open(fb_file).readlines()[0:]]    # web sear>
DINT_4_95_fb = [float(line.split()[12]) for line in open(fb_file).readlines()[0:]]    # web sear>
DINT_4_99_fb = [float(line.split()[13]) for line in open(fb_file).readlines()[0:]]    # web sear>

fb_x_axis = [int(line.split()[1]) for line in open(fb_file).readlines()[0:]] # fb flow sizes

# Print the DINT_1_95_fb list (for verification)
print("DINT_1_95_fb:", DINT_1_95_fb)

# Calculate and print the median of DINT_1_95_fb
median_DINT_1_95_fb = median(DINT_1_95_fb)
print("Median of DINT_1_95_fb:", median_DINT_1_95_fb)

# Print the DINT_2_95_fb list (for verification)
print("DINT_2_95_fb:", DINT_2_95_fb)

# Calculate and print the median of DINT_2_95_fb
median_DINT_2_95_fb = median(DINT_2_95_fb)
print("Median of DINT_2_95_fb:", median_DINT_2_95_fb)

# Print the DINT_3_95_fb list (for verification)
print("DINT_3_95_fb:", DINT_3_95_fb)

# Calculate and print the median of DINT_3_95_fb
median_DINT_3_95_fb = median(DINT_3_95_fb)
print("Median of DINT_3_95_fb:", median_DINT_3_95_fb)

# Print the DINT_4_95_fb list (for verification)
print("DINT_4_95_fb:", DINT_4_95_fb)

# Calculate and print the median of DINT_4_95_fb
median_DINT_4_95_fb = median(DINT_4_95_fb)
print("Median of DINT_4_95_fb:", median_DINT_4_95_fb)

plt.plot(np.linspace(0, 10, num=20),DINT_1_95_fb, color='red', linestyle='-', label='DINT k = 16',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),DINT_2_95_fb, color='blue', linestyle='--', label='DINT k = 8',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),DINT_3_95_fb, color='green', linestyle='-.', label='DINT k = 4',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),DINT_4_95_fb, color='purple', linestyle=':', label='DINT k = 2',linewidth=4.0)
# Set the y-axis limit


ax.set_xticks(range(1,11))
ax.set_xticklabels([str(x) if x < 1000 else str(int(x/1000. + .5)) + 'K' if x < 1000.**2 else str(int(x/1000.**2 + .5)) + 'M' for x in fb_x_axis[1::2]])


plt.legend(bbox_to_anchor=(0.5, 1.2),loc='upper center',ncol=2)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='y', which='major', labelsize=23)
plt.ylabel(r'Slowdown', fontsize=10)
plt.xlabel('Flow Size [Bytes]', fontsize=28)
#plt.xlim([0, maxPkts])
plt.tight_layout()
plt.savefig('facebook_95p.png')
exit()