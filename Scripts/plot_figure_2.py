# 
# Code for analysing rocket body reentries
# by etwright1 (E. Wright), 2022
#

import numpy as np
import matplotlib.pylab as plt

wf600 = np.genfromtxt('Casexp_RBs_p600_050522.csv_weighting_function')
wf10 = np.genfromtxt('rb decayed 1992-2021 7 days_weighting function.csv') / 3

latitudes = list(reversed(np.arange(-90, 90, 0.5)))

fontsize = 6
plt.figure(figsize=(4, 2.375), dpi=300)
plt.rc('font', size=fontsize)  
plt.plot(latitudes, wf600, label= 'In orbit with perigee < 600', color='#355C7D')
plt.plot(latitudes, wf10, label='10 year projection', color='#F67280', linestyle=(0, (1, 1)))
plt.xlabel("Latitude (deg)", color='#000000')
plt.ylabel('Weighting function (unitless)', color='#000000')
plt.xticks(np.arange(-90, 110, 30))
plt.grid(b=True, alpha=0.25)
plt.xlim((-90,90))
plt.legend(loc=2)
plt.ylim((0,12))
plt.tight_layout()
plt.savefig('Figure 2.svg')
plt.show()
