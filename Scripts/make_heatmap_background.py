# 
# Code for analysing rocket body reentries
# by etwright1 (E. Wright), 2022
#

import numpy as np
import matplotlib.pylab as plt

weighting_function = np.genfromtxt("Output data/Casexp_RBs_p600_050522.csv_weighting_function", delimiter=",") 

heatmap = np.ones((360,720))

for x in range(720):
    heatmap[:,x] = weighting_function

fontsize = 6
plt.figure(figsize=(4.75, 2.375),dpi=300)
plt.rc('font', size=fontsize)
plt.pcolormesh(np.log10(heatmap), cmap = 'Blues', vmin = -1.5) 
plt.colorbar()
plt.gca().invert_yaxis()
plt.savefig('heatmap_image.png', bbox_inches='tight', pad_inches=0)
plt.show()
