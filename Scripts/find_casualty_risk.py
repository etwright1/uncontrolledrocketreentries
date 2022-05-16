# 
# Code for analysing rocket body reentries
# by etwright1 (E. Wright), 2022
#

import numpy as np
import matplotlib.pylab as plt
import casualty as cs

RE=6378000 # equatorial radius in m

latitudes = list(reversed(np.arange(-90, 90, 0.5))) #create latitudes list
weighting_function = np.zeros(360)

file = "Input data/RBs_p600_050522.csv" #define inclinations input file
satellite_inclinations = np.genfromtxt(file)

casualty_expectation_file = "Casexp_" + file #create output filenames
weighting_function_file = casualty_expectation_file + "_weighting_function"

num_of_satellites = len(satellite_inclinations)
timer = 0
limit = 0

#create weighting function

for x in satellite_inclinations:
    if x > limit:
        if x > 90:
            x = 180 - x

        vals, lats = cs.latWeights(0.5, 550e3+RE, x) #get latitude weights

        weighting_function += vals #add the normalised times

        timer +=1
        print("Working on satellite:", timer, "of", num_of_satellites)

np.savetxt(weighting_function_file, weighting_function) #save latweights function

#find casualty expectation

GPW4 = np.genfromtxt("Input data/GPW4_2020.csv", delimiter=' ') #import and clean GPW4 population data
GPW4 = np.where(GPW4==-9999, 0, GPW4)

print("Sanity check: Population of Earth in 2020= ", np.sum(np.sum(GPW4)))

heatmap = np.ones((360,720))

for x in range(720): # across all longitudes
    heatmap[:,x] = GPW4[:,x] * weighting_function # Two dimensional, this is a slightly convoluted method

casualty_by_latitude = heatmap.sum(axis=1) #back to one dimension

area_of_latitude_band = np.ones(len(latitudes))
casualty_expectation = np.ones(len(latitudes))

for x in range(len(latitudes)): #dividing by latitude band area to get casualty expectation
    upper_latitude = abs(90 - x/2) 
    lower_latitude = abs(90 - x/2 + 0.5)
    area_of_latitude_band[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_latitude)) - np.sin(np.deg2rad(lower_latitude))))
    casualty_expectation[x] =  casualty_by_latitude[x] / area_of_latitude_band[x]

print('Sanity check: Earth area = ', sum(area_of_latitude_band))
print("Total risk for", file, "is", sum(casualty_expectation) )

np.savetxt(casualty_expectation_file, casualty_expectation)

plt.figure()
plt.plot(latitudes, casualty_expectation)
plt.xlabel("Latitude (deg)")
plt.ylabel("Casualty expectation (# m$^-$$^2$)")
plt.xticks(np.arange(-90, 110, 20))
plt.show()


