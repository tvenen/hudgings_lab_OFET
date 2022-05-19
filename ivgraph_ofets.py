import matplotlib.pyplot as plt
import pandas as pd
import os
from glob import glob

maindir = '/Users/taylorvenenciano/Desktop/OFET_IV'
subdir = '4_14_OFETs'
subsubdir = 'Run 1' # will graph all files ending in .txt in this folder name, labeled as 1_10V.txt
all_dir = glob(os.path.join(maindir, subdir, subsubdir, "*.txt")) #adjust to determine directory
sort = sorted(all_dir) # ordering data so that legend is nice

for item in sort:
    frame = pd.read_table(item)
    volt = frame['Voltage (V)']
    curr = frame['Current (A)']
    curr_micro = pd.to_numeric(curr)*(10**6) # changing unit to microA
    name = os.path.split(item)[1] #using name of file for legend
    name2 = name.split('_')[1] #modify here for naming convention
    name3 = name2.split('.')[0]#modify here for naming convention
    plt.plot(volt, -curr_micro, label = name3) #if current is positive, put negative curr_micro, change label for legend
    
plt.xlabel('Voltage (V)')
plt.ylabel('Current (\N{MICRO SIGN}A)')
plt.title('IV Curves ' + subdir) #adjust title of graph
plt.xlim([40,0]) #adjust x-range
plt.ylim([-60,0]) #adjust y-range
plt.legend()
plt.show()