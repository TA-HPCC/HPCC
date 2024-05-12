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

#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['pdf.use14corefonts'] = True
#matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
    
fig, ax = plt.subplots(figsize=(10,5))    

plt.grid()
plt.gcf().subplots_adjust(bottom=0.15)

wb_file = 'fct_wb50_all_dint.dat'


DINT_alfa15_50_wb = [float(line.split()[2]) for line in open(wb_file).readlines()[0:]]     # web search
DINT_alfa15_95_wb = [float(line.split()[3]) for line in open(wb_file).readlines()[0:]]     # web search
DINT_alfa15_99_wb = [float(line.split()[4]) for line in open(wb_file).readlines()[0:]]     # web search
DINT_alfa125_50_wb = [float(line.split()[5]) for line in open(wb_file).readlines()[0:]]    # web search
DINT_alfa125_95_wb = [float(line.split()[6]) for line in open(wb_file).readlines()[0:]]    # web search
DINT_alfa125_99_wb = [float(line.split()[7]) for line in open(wb_file).readlines()[0:]]    # web search
DINT_alfa1125_50_wb = [float(line.split()[8]) for line in open(wb_file).readlines()[0:]]    # web sear>
DINT_alfa1125_95_wb = [float(line.split()[9]) for line in open(wb_file).readlines()[0:]]    # web sear>
DINT_alfa1125_99_wb = [float(line.split()[10]) for line in open(wb_file).readlines()[0:]]    # web sear>
DINT_alfa10675_50_wb = [float(line.split()[11]) for line in open(wb_file).readlines()[0:]]    # web sear>
DINT_alfa10675_95_wb = [float(line.split()[12]) for line in open(wb_file).readlines()[0:]]    # web sear>
DINT_alfa10675_99_wb = [float(line.split()[13]) for line in open(wb_file).readlines()[0:]]    # web sear>
wb_x_axis = [int(line.split()[1]) for line in open(wb_file).readlines()[0:]] # wb flow sizes


plt.plot(np.linspace(0, 10, num=20),DINT_alfa15_95_wb, color='red', linestyle='-', label='DINT alfa = 1.5',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),DINT_alfa125_95_wb, color='blue', linestyle='--', label='DINT alfa = 1.25 (original)',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),DINT_alfa1125_95_wb, color='green', linestyle='-.', label='DINT alfa = 1.125',linewidth=4.0)
plt.plot(np.linspace(0, 10, num=20),DINT_alfa10675_95_wb, color='purple', linestyle=':', label='DINT alfa = 1.0675',linewidth=4.0)
plt.ylim([1,11])
ax.set_xticks(range(1,11))
ax.set_xticklabels([str(x) if x < 1000 else str(int(x/1000. + .5)) + 'K' if x < 1000.**2 else str(int(x/1000.**2 + .5)) + 'M' for x in wb_x_axis[1::2]])


plt.legend(bbox_to_anchor=(0.5, 1.2),loc='upper center',ncol=2)
plt.tick_params(axis='both', which='major', labelsize=18)
plt.tick_params(axis='y', which='major', labelsize=23)
plt.ylabel(r'Slowdown', fontsize=28)    
plt.xlabel('Flow Size [Bytes]', fontsize=28)
#plt.xlim([0, maxPkts])
plt.tight_layout()
plt.savefig('web_search_95p.pdf')
plt.savefig('web_search_95p.png')
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