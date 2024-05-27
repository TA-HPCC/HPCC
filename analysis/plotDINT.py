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
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('-param', dest='param', action='store', default='k', help="alpha / k")
parser.add_argument('-topo', dest='topo', action='store', default='fat')
parser.add_argument('-traf', dest='traffic', action='store', default='fb', help="fb or wb")
args = parser.parse_args()

param = args.param
topo = args.topo
traf = args.traffic
#matplotlib.rcParams['ps.useafm'] = True
#matplotlib.rcParams['pdf.use14corefonts'] = True
#matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
    
fig, ax = plt.subplots(figsize=(10,5))    

plt.grid()
plt.gcf().subplots_adjust(bottom=0.15)

file = 'fct_' + traf + '50_' + param + '_dint_' + topo + '.dat'

DINT_1_50 = [float(line.split()[2]) for line in open(file).readlines()[0:]]     # web search
DINT_1_95 = [float(line.split()[3]) for line in open(file).readlines()[0:]]     # web search
DINT_1_99 = [float(line.split()[4]) for line in open(file).readlines()[0:]]     # web search
DINT_2_50 = [float(line.split()[5]) for line in open(file).readlines()[0:]]    # web search
DINT_2_95 = [float(line.split()[6]) for line in open(file).readlines()[0:]]    # web search
DINT_2_99 = [float(line.split()[7]) for line in open(file).readlines()[0:]]    # web search
DINT_3_50 = [float(line.split()[8]) for line in open(file).readlines()[0:]]    # web sear>
DINT_3_95 = [float(line.split()[9]) for line in open(file).readlines()[0:]]    # web sear>
DINT_3_99 = [float(line.split()[10]) for line in open(file).readlines()[0:]]    # web sear>
DINT_4_50 = [float(line.split()[11]) for line in open(file).readlines()[0:]]    # web sear>
DINT_4_95 = [float(line.split()[12]) for line in open(file).readlines()[0:]]    # web sear>
DINT_4_99 = [float(line.split()[13]) for line in open(file).readlines()[0:]]    # web sear>
fb_x_axis = [int(line.split()[1]) for line in open(file).readlines()[0:]] # fb flow sizes

if param == 'alpha' :
    # Print the DINT_1_95_fb list (for verification)
    print "DINT alpha 1.5:", DINT_1_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_alpha15_95_fb = sum(DINT_1_95) / len(DINT_1_95)
    print "Average of DINT alpha 1.5:", average_DINT_alpha15_95_fb

    # Print the DINT_1_95_fb list (for verification)
    print "DINT alpha 1.25:", DINT_2_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_alpha125_95_fb = sum(DINT_2_95) / len(DINT_2_95)
    print "Average of DINT alpha 1.25:", average_DINT_alpha125_95_fb

    # Print the DINT_1_95_fb list (for verification)
    print "DINT alpha 1.125:", DINT_3_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_alpha1125_95_fb = sum(DINT_3_95) / len(DINT_3_95)
    print "Average of DINT alpha 1.125:", average_DINT_alpha1125_95_fb

    # Print the DINT_1_95_fb list (for verification)
    print "DINT alpha 1.0675:", DINT_4_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_alpha10675_95_fb = sum(DINT_4_95) / len(DINT_4_95)
    print "Average of DINT alpha 1.0675:", average_DINT_alpha10675_95_fb
    
    plt.plot(np.linspace(0, 10, num=20),DINT_1_95, color='red', linestyle='-', label='DINT alpha = 1.5',linewidth=4.0)
    plt.plot(np.linspace(0, 10, num=20),DINT_2_95, color='blue', linestyle='--', label='DINT alpha = 1.25',linewidth=4.0)
    plt.plot(np.linspace(0, 10, num=20),DINT_3_95, color='green', linestyle='-.', label='DINT alpha = 1.125',linewidth=4.0)
    plt.plot(np.linspace(0, 10, num=20),DINT_4_95, color='purple', linestyle=':', label='DINT alpha = 1.0675',linewidth=4.0)
    
elif param == 'k' :
    # Print the DINT_1_95_fb list (for verification)
    print "DINT k 16:", DINT_1_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_k16_95_fb = sum(DINT_1_95) / len(DINT_1_95)
    print "Average of DINT k 16:", average_DINT_k16_95_fb

    # Print the DINT_1_95_fb list (for verification)
    print "DINT k 8:", DINT_2_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_k8_95_fb = sum(DINT_2_95) / len(DINT_2_95)
    print "Average of DINT k 8:", average_DINT_k8_95_fb

    # Print the DINT_1_95_fb list (for verification)
    print "DINT k 4:", DINT_3_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_k4_95_fb = sum(DINT_3_95) / len(DINT_3_95)
    print "Average of DINT k 4:", average_DINT_k4_95_fb

    # Print the DINT_1_95_fb list (for verification)
    print "DINT k 2:", DINT_4_95

    # Calculate and print the average of DINT_4_95_fb
    average_DINT_k2_95_fb = sum(DINT_4_95) / len(DINT_4_95)
    print "Average of DINT k 2:", average_DINT_k2_95_fb
    
    plt.plot(np.linspace(0, 10, num=20),DINT_1_95, color='red', linestyle='-', label='DINT k = 16',linewidth=4.0)
    plt.plot(np.linspace(0, 10, num=20),DINT_2_95, color='blue', linestyle='--', label='DINT k = 8',linewidth=4.0)
    plt.plot(np.linspace(0, 10, num=20),DINT_3_95, color='green', linestyle='-.', label='DINT k = 4',linewidth=4.0)
    plt.plot(np.linspace(0, 10, num=20),DINT_4_95, color='purple', linestyle=':', label='DINT k = 2',linewidth=4.0)


plt.ylim([1,11])
ax.set_xticks(range(1,11))
ax.set_xticklabels([str(x) if x < 1000 else str(int(x/1000. + .5)) + 'K' if x < 1000.**2 else str(int(x/1000.**2 + .5)) + 'M' for x in fb_x_axis[1::2]])

output_file = traf + '_dint_' + topo + '_' + param
plt.legend(bbox_to_anchor=(0.5, 1.2),loc='upper center',ncol=2)
plt.tick_params(axis='both', which='major', labelsize=18)
plt.tick_params(axis='y', which='major', labelsize=23)
plt.ylabel(r'Slowdown', fontsize=28)    
plt.xlabel('Flow Size [Bytes]', fontsize=28)
#plt.xlim([0, maxPalphats])
plt.tight_layout()
plt.savefig(output_file+'.pdf')
plt.savefig(output_file+'.png')
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
            #plt.plot(xrange(maxPalphats+2),[alpha]+hybridAverages[p2][i], linestyle, label='Hybrid('+str(p2)+')')
            linestyle = '-'
            plt.plot(xrange(maxPalphats+2),[alpha]+hybridAverages[p2][i], linestyle, label='Hybrid',linewidth=4.0)
            #plt.plot(xrange(maxPalphats+2),[alpha]+hybridAverages[p2][i], linestyle, label='Hybrid('+str(p2)+','+str(a)+')')
    p = a/alpha
    #print histogram, 
    #print averages[i], p           
    #plt.plot(xrange(maxPalphats+1),averages[i], linestyle, label=str(a) + ' / alpha')
    #plt.plot(xrange(maxPalphats+2),[alpha]+averages[i], linestyle, label='XOR('+str(p)+')')
    #plt.plot(xrange(maxPalphats+2),[alpha]+averages[i], linestyle, label='XOR')
    if True:
        #plt.plot(xrange(maxPalphats+2),[alpha]+averages[i], linestyle, label='XOR('+str(a)+')')
        if a != 1:
            continue
        linestyle = '--'
        plt.plot(xrange(maxPalphats+2),[alpha]+averages[i], linestyle, label='XOR',linewidth=4.0)
    sys.stdout.flush()

        
linestyle = ':'    
plt.plot(xrange(maxPalphats+1),averagesCC, linestyle, label='Baseline',linewidth=4.0)    
plt.legend(loc='best',prop={'size':24},ncol=1)
plt.ticalpha_params(axis='both', which='major', labelsize=28)
plt.ylabel(r'$E$[Missing Hops]', fontsize=28)    
plt.xlabel('Number of Pacalphaets', fontsize=28)
plt.xlim([0, maxPalphats])
plt.savefig(fName+'.pdf')
plt.savefig(fName+'.png')
#plt.show()