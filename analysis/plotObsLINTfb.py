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

fb_file = 'fct_fb50_all_lint.dat'


LINT_1_50_fb = [float(line.split()[2]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_1_95_fb = [float(line.split()[3]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_1_99_fb = [float(line.split()[4]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_2_50_fb = [float(line.split()[5]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_2_95_fb = [float(line.split()[6]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_2_99_fb = [float(line.split()[7]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_3_50_fb = [float(line.split()[8]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_3_95_fb = [float(line.split()[9]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_3_99_fb = [float(line.split()[10]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_4_50_fb = [float(line.split()[11]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_4_95_fb = [float(line.split()[12]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_4_99_fb = [float(line.split()[13]) for line in open(fb_file).readlines()[0:]]    # web sear>

fb_x_axis = [int(line.split()[1]) for line in open(fb_file).readlines()[0:]] # fb flow sizes


plt.plot(np.linspace(0, 10, num=20),LINT_1_95_fb, color='red', linestyle='-', label='LINT obs_window = 1 micro s',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),LINT_2_95_fb, color='blue', linestyle='--', label='LINT obs_window = 10 micros',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),LINT_3_95_fb, color='green', linestyle='-.', label='LINT obs_window = 100 micro s',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),LINT_4_95_fb, color='purple', linestyle=':', label='LINT obs_window = 1 ms',linewidth=4.0)


ax.set_xticks(range(1,11))
ax.set_xticklabels([str(x) if x < 1000 else str(int(x/1000. + .5)) + 'K' if x < 1000.**2 else str(int(x/1000.**2 + .5)) + 'M' for x in fb_x_axis[1::2]])

# Print the LINT_1_95_fb list (for verification)
print "LINT_1_95_fb:", LINT_1_95_fb

# Calculate and print the average of LINT_4_95_fb
average_LINT_1_95_fb = sum(LINT_1_95_fb) / len(LINT_1_95_fb)
print "Average of LINT_1_95_fb:", average_LINT_1_95_fb

# Print the LINT_2_95_fb list (for verification)
print "LINT_2_95_fb:", LINT_2_95_fb

# Calculate and print the average of LINT_2_95_fb
average_LINT_2_95_fb = sum(LINT_2_95_fb) / len(LINT_2_95_fb)
print "Average of LINT_2_95_fb:", average_LINT_2_95_fb

# Print the LINT_3_95_fb list (for verification)
print "LINT_3_95_fb:", LINT_3_95_fb

# Calculate and print the average of LINT_4_95_fb
average_LINT_3_95_fb = sum(LINT_3_95_fb) / len(LINT_3_95_fb)
print "Average of LINT_3_95_fb:", average_LINT_3_95_fb

# Print the LINT_4_95_fb list (for verification)
print "LINT_4_95_fb:", LINT_4_95_fb

# Calculate and print the average of LINT_4_95_fb
average_LINT_4_95_fb = sum(LINT_4_95_fb) / len(LINT_4_95_fb)
print "Average of LINT_4_95_fb:", average_LINT_4_95_fb

plt.legend(bbox_to_anchor=(0.5, 1.2),loc='upper center',ncol=2)
plt.tick_params(axis='both', which='major', labelsize=18)
plt.tick_params(axis='y', which='major', labelsize=23)
plt.ylabel(r'Slowdown', fontsize=28)    
plt.xlabel('Flow Size [Bytes]', fontsize=28)
#plt.xlim([0, maxPkts])
plt.tight_layout()
plt.savefig('facebook_95p.pdf')
plt.savefig('facebook_95p.png')
exit()
