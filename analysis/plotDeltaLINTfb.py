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

fb_file = 'fct_fb50_all_lint_delta.dat'


LINT_1_50_fb = [float(line.split()[2]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_1_95_fb = [float(line.split()[3]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_1_99_fb = [float(line.split()[4]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_2_50_fb = [float(line.split()[5]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_2_95_fb = [float(line.split()[6]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_2_99_fb = [float(line.split()[7]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_3_50_fb = [float(line.split()[8]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_3_95_fb = [float(line.split()[9]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_3_99_fb = [float(line.split()[10]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_4_50_fb = [float(line.split()[11]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_4_95_fb = [float(line.split()[12]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_4_99_fb = [float(line.split()[13]) for line in open(fb_file).readlines()[0:]]     # web search
LINT_5_50_fb = [float(line.split()[14]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_5_95_fb = [float(line.split()[15]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_5_99_fb = [float(line.split()[16]) for line in open(fb_file).readlines()[0:]]    # web search
LINT_6_50_fb = [float(line.split()[17]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_6_95_fb = [float(line.split()[18]) for line in open(fb_file).readlines()[0:]]    # web sear>
LINT_6_99_fb = [float(line.split()[19]) for line in open(fb_file).readlines()[0:]]    # web sear>

fb_x_axis = [int(line.split()[1]) for line in open(fb_file).readlines()[0:]] # fb flow sizes

# Print the LINT_1_95_fb list (for verification)
print("LINT_1_95_fb:", LINT_1_95_fb)

# Calculate and print the median of LINT_1_95_fb
median_LINT_1_95_fb = median(LINT_1_95_fb)
print("Median of LINT_1_95_fb:", median_LINT_1_95_fb)

# Print the LINT_2_95_fb list (for verification)
print("LINT_2_95_fb:", LINT_2_95_fb)

# Calculate and print the median of LINT_2_95_fb
median_LINT_2_95_fb = median(LINT_2_95_fb)
print("Median of LINT_2_95_fb:", median_LINT_2_95_fb)

# Print the LINT_3_95_fb list (for verification)
print("LINT_3_95_fb:", LINT_3_95_fb)

# Calculate and print the median of LINT_3_95_fb
median_LINT_3_95_fb = median(LINT_3_95_fb)
print("Median of LINT_3_95_fb:", median_LINT_3_95_fb)

# Print the LINT_4_95_fb list (for verification)
print("LINT_4_95_fb:", LINT_4_95_fb)

# Calculate and print the median of LINT_4_95_fb
median_LINT_4_95_fb = median(LINT_4_95_fb)
print("Median of LINT_4_95_fb:", median_LINT_4_95_fb)

# Print the LINT_5_95_fb list (for verification)
print("LINT_5_95_fb:", LINT_5_95_fb)

# Calculate and print the median of LINT_5_95_fb
median_LINT_5_95_fb = median(LINT_5_95_fb)
print("Median of LINT_5_95_fb:", median_LINT_5_95_fb)

# Print the LINT_6_95_fb list (for verification)
print("LINT_6_95_fb:", LINT_6_95_fb)

# Calculate and print the median of LINT_6_95_fb
median_LINT_6_95_fb = median(LINT_6_95_fb)
print("Median of LINT_6_95_fb:", median_LINT_6_95_fb)

plt.plot(np.linspace(0, 10, num=20),LINT_1_95_fb, color='red', linestyle='-', label='LINT delta = 1',linewidth=2.0)
plt.plot(np.linspace(0, 10, num=20),LINT_2_95_fb, color='blue', linestyle='--', label='LINT delta = 2',linewidth=2.0)
plt.plot(np.linspace(0, 10, num=20),LINT_3_95_fb, color='green', linestyle='-.', label='LINT delta = 3',linewidth=2.0)
plt.plot(np.linspace(0, 10, num=20),LINT_4_95_fb, color='purple', linestyle=':', label='LINT delta = 4',linewidth=2.0)
plt.plot(np.linspace(0, 10, num=20),LINT_5_95_fb, color='orange', linestyle='-', label='LINT delta = 5',linewidth=2.0)
plt.plot(np.linspace(0, 10, num=20),LINT_6_95_fb, color='brown', linestyle='--', label='LINT delta = 6',linewidth=2.0)

ax.set_xticks(range(1,11))
ax.set_xticklabels([str(x) if x < 1000 else str(int(x/1000. + .5)) + 'K' if x < 1000.**2 else str(int(x/1000.**2 + .5)) + 'M' for x in fb_x_axis[1::2]])


plt.legend(bbox_to_anchor=(0.5, 1.2),loc='upper center',ncol=2)
plt.tick_params(axis='both', which='major', labelsize=18)
plt.tick_params(axis='y', which='major', labelsize=23)
plt.ylabel(r'Slowdown', fontsize=28)    
plt.xlabel('Flow Size [Bytes]', fontsize=28)
#plt.xlim([0, maxPkts])
plt.tight_layout()
plt.savefig('facebook_95p.png')
exit()

HPCC = 0

#plt.tight_layout()
#for p in pRange:
#print histogram, 
for i,a in enumerate(aRange):
    linestyle = '-' if i < 3 else '--'
    if True:
        for j,p2 in enumerate(p2Range):
            if j > 2:
                linestyle = ':'
            if a != 7.75:
                continue
            #print 'HERE', hybridAverages
            #plt.plot(xrange(maxPkts+2),[k]+hybridAverages[p2][i], linestyle, label='Hybrid('+str(p2)+')')
            linestyle = '-'
            plt.plot(xrange(maxPkts+2),[k]+hybridAverages[p2][i], linestyle, label='Hybrid',linewidth=4.0)
            #plt.plot(xrange(maxPkts+2),[k]+hybridAverages[p2][i], linestyle, label='Hybrid('+str(p2)+','+str(a)+')')
    p = a/k
    #print histogram, 
    #print averages[i], p           
    #plt.plot(xrange(maxPkts+1),averages[i], linestyle, label=str(a) + ' / k')
    #plt.plot(xrange(maxPkts+2),[k]+averages[i], linestyle, label='XOR('+str(p)+')')
    #plt.plot(xrange(maxPkts+2),[k]+averages[i], linestyle, label='XOR')
    if True:
        #plt.plot(xrange(maxPkts+2),[k]+averages[i], linestyle, label='XOR('+str(a)+')')
        if a != 1:
            continue
        linestyle = '--'
        plt.plot(xrange(maxPkts+2),[k]+averages[i], linestyle, label='XOR',linewidth=4.0)
    sys.stdout.flush()

        
linestyle = ':'    
plt.plot(xrange(maxPkts+1),averagesCC, linestyle, label='Baseline',linewidth=4.0)    
plt.legend(loc='best',prop={'size':24},ncol=1)
plt.tick_params(axis='both', which='major', labelsize=28)
plt.ylabel(r'$E$[Missing Hops]', fontsize=28)    
plt.xlabel('Number of Packets', fontsize=28)
plt.xlim([0, maxPkts])
plt.savefig(fName+'.pdf')
plt.savefig(fName+'.png')
#plt.show()