import numpy as np
import matplotlib.pylab as plt

RE=6378000 # equatorial radius in m

adjusted_risk = np.genfromtxt("Casexp_RBs_p600_050522.csv", delimiter=' ') #import risk weighting
population = np.genfromtxt("GPW4_2020.csv", delimiter=' ') #import and clean GPW4 population data
population = np.where(population==-9999, 0, population) 

latitude_population = population.sum(axis=1) #sum cells to get population per latitude 
latitudes = list(reversed(np.arange(-90, 90, 0.5)))
latitude_bins = len(latitude_population)

area_of_lat = np.ones(latitude_bins) #intialising 
population_density = np.ones(latitude_bins)

for x in range(latitude_bins):
    upper_lat = abs(90 - x/2) # define latitude bins
    lower_lat = abs(90 - x/2 + 0.5)
    area_of_lat[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_lat)) - np.sin(np.deg2rad(lower_lat)))) 
    population_density[x] = latitude_population[x] / area_of_lat[x] #Unit is now people / m^2

print('Sense check 2: Earth Surface Area = ', int(sum(area_of_lat)/1e12), 'trillion m ^2')

fontsize = 6
plt.figure(figsize=(2.375, 2.375), dpi=300)
plt.rc('font', size=fontsize)          # controls default text sizes
plt.plot(latitudes, adjusted_risk*1e4, label= 'Casualty expectation', color='#355C7D')
plt.plot(latitudes, population_density*1e4, label='Population density', color='#F67280', linestyle=(0, (1, 1)))
plt.xlabel("Latitude (deg)", color='#000000')
plt.ylabel('Number per m$^2$,   x10$^-$$^4$', color='#000000')
plt.xticks(np.arange(-90, 110, 30))
plt.grid(b=True, alpha=0.25)
plt.xlim((-90,90))
plt.legend(loc=2)
plt.ylim((0,3))
plt.ticklabel_format(axis="y", style="scientific", scilimits=(0,0))
plt.tight_layout()
plt.savefig('Figure 1D.svg')
plt.show()