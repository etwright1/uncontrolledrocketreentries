# 
# Code for analysing rocket body reentries
# by etwright1 (E. Wright), 2022
#

import numpy as np
import matplotlib.pylab as plt
import casualty as cs

RE=6378000 # equatorial radius in m

GPW4 = np.genfromtxt("Input data/GPW4_2020.csv", delimiter=' ') # import data as array. GPW4 2020 count data, half degree resolution
GPW4refined = np.where(GPW4==-9999, 0, GPW4) # turn no data (=-9999) into 0s

lat_bin_sum = GPW4refined.sum(axis=1) # sum rows and sum columns. Unit is people
long_bin_sum = GPW4refined.sum(axis=0)
longitude_bins = len(long_bin_sum)
latitude_bins = len(lat_bin_sum)

print('Sense check 1: World Population = ', int(sum(lat_bin_sum)/1e6), 'million people')

area_of_lat = np.ones(latitude_bins) 
pop_den = np.ones(latitude_bins)

for x in range(latitude_bins):
    upper_lat = abs(90 - x/2) # define latitude bins
    lower_lat = abs(90 - x/2 + 0.5)
    area_of_lat[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_lat)) - np.sin(np.deg2rad(lower_lat)))) 
    pop_den[x] = lat_bin_sum[x] / area_of_lat[x] # Unit is now people / m^2

print('Sense check 2: Earth Surface Area = ', int(sum(area_of_lat)/1e12), 'trillion m ^2')

inc_resolution = 0.5
orbit_inclinations = list(np.arange(0,90+inc_resolution, inc_resolution)) # create lattitude array
orbit_inc_bins = len(orbit_inclinations)
total_casexp = np.zeros(0)

for x in orbit_inclinations:
    vals, lats = cs.latWeights(0.5, 550e3+RE, x) # get time weighting 
    weighted_pop_den = np.multiply(pop_den, vals) # unit is population density
    total_casexp_per_inc = np.sum(weighted_pop_den) # summing population density values for each orbit inclination
    total_casexp = np.append(total_casexp, total_casexp_per_inc)
    print('Working on inclination:', x)

np.savetxt("incl vs casexp 2020 results", total_casexp)

fontsize = 6
plt.figure(figsize=(2.375, 2.375), dpi=300)
plt.rc('font', size=fontsize)

plt.plot(orbit_inclinations, total_casexp*1e5, '#355C7D')
plt.xlabel("Orbit inclination (deg)", color='#000000')
plt.ylabel("Number per m$^2$,   x10$^-$$^5$", color='#000000')
plt.ticklabel_format(axis="y", style="scientific", scilimits=(0,0))
plt.grid(b=True, alpha=0.25)
plt.xlim((0,90))

plt.xticks(np.arange(0, 110, 30))
plt.tight_layout()
plt.savefig('Figure 1C.svg')
plt.show()
