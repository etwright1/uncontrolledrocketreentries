import matplotlib.pyplot as plt
import numpy as np

RE=6378000 # equatorial radius in m

GPW4 = np.genfromtxt("Input data/GPW4_2020.csv", delimiter=' ') # import and clean GPW4 population data
population = np.where(GPW4==-9999, 0, GPW4) 

population_by_latitude = population.sum(axis=1) # sum cells to get population per latitude 
latitudes = list(reversed(np.arange(-90, 90, 0.5)))
latitude_bins = len(population_by_latitude)

area_of_latitude_band = np.ones(latitude_bins) 
population_density = np.ones(latitude_bins)

for x in range(latitude_bins):
    upper_latitude = abs(90 - x/2) # define latitude bins
    lower_latitude = abs(90 - x/2 + 0.5)
    area_of_latitude_band[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_latitude)) - np.sin(np.deg2rad(lower_latitude)))) 
    population_density[x] = population_by_latitude[x] / area_of_latitude_band[x] #Unit is now people / m^2

fontsize = 6
img = plt.imread('Images and plots/heatmap_cropped_with_borders.tif')
plt.rc('font', size=fontsize)

fig, ax1 = plt.subplots(figsize=(4.75*0.75, 2.375), dpi=300)
ax1.imshow(img, aspect='auto',  extent=[0, 10, -90, 90])
ax1.set_yticks(np.arange(-90, 110, 30))
ax1.get_xaxis().set_visible(False)
ax1.set_ylabel("Latitude (deg)", fontsize = fontsize)
ax1.tick_params(axis='y', labelsize=fontsize)

ax2 = ax1.twiny()
ax2.plot(population_density*1e5, latitudes, color='#FFA500', linewidth=1)
ax2.set_xlabel("Population density (# m$^-$$^2$)   x10$^-$$^5$", fontsize = fontsize)
ax2.set_xlim(0,8)
ax2.tick_params(axis='x', labelsize=fontsize) 

plt.tight_layout()
plt.savefig("heatmap_without_legend.svg")
plt.show()