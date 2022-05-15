import numpy as np
import csv
import matplotlib.pylab as plt
import datetime
import casualty as cs

satcat = csv.reader(open("satcat 5 May 2022.csv", "r"), delimiter=",")

filename = "rb decayed 1992-2021 7 days"
population_file = "Input data/GPW4_2005.csv"
array = []
cutoffdate = '1992-05-05' #thiry years before date of analysis
cutoffdate = datetime.datetime.strptime(cutoffdate, "%Y-%m-%d")

#filtering for RBs, decayed after 05/05/1992, with known inclination

for row in satcat:
    if row[3] == "R/B":
        if row[4] == "D":
            launch_date = row[6]
            launch_date = datetime.datetime.strptime(launch_date,'%Y-%m-%d')
            decay_date = row[8]
            decay_date = datetime.datetime.strptime(decay_date,'%Y-%m-%d')
            difference = decay_date - launch_date
            if decay_date > cutoffdate:
                if row[10] != '':
                    if difference.days >= 7:
                        array.append(row)

print(f"There are {len(array)} RBs decayed at or after 7 days and launched in the last 30 years with known inclinations")

#casualty expectation code
array = np.array(array)

sat_incs = []
for row in array:
    sat_incs.append(float(row[10])) 

satellite_inclination_file = filename + ' inclinations.csv'
np.savetxt(satellite_inclination_file, sat_incs)

RE=6378000 # equatorial radius in m
latitudes = list(reversed(np.arange(-90, 90, 0.5))) #create latitudes list
weighting_function = np.zeros(360)

casualty_expectation = filename #for output filenames
weighting_function_file = filename + "_weighting function.csv"
num_of_satellites = len(sat_incs)
timer = 0
limit = int(0)

for x in sat_incs:
    if x > limit:
        if x > 90:
            x = 180 - x

        vals, lats = cs.latWeights(0.5, 550e3+RE, x) #get latitude weights

        weighting_function += vals #add the normalised times

        timer +=1
        print("Working on satellite:", timer, "of", num_of_satellites)

np.savetxt(weighting_function_file, weighting_function) #save weighting function

GPW4 = np.genfromtxt(population_file, delimiter=' ') #import and clean GPW4 data
GPW4 = np.where(GPW4==-9999, 0, GPW4)
population = np.where(GPW4==-9999, 0, GPW4) 

latitude_population = population.sum(axis=1) #sum cells to get population per latitude 
latitudes = list(reversed(np.arange(-90, 90, 0.5)))
latitude_bins = len(latitude_population)

print("Sanity check: Population of Earth in 2005 = ", np.sum(np.sum(GPW4)))

heatmap = np.ones((360,720))

for x in range(720):
    heatmap[:,x] = GPW4[:,x] * weighting_function # 2D, this is a convoluted way of doing this

casualty_by_latitude = heatmap.sum(axis=1) #back to 1D

population_density = np.ones(latitude_bins)
area_of_latitude_band = np.ones(len(latitudes)) # initialising
casualty_expectation = np.ones(len(latitudes))

for x in range(len(latitudes)): #dividing by area to get casualty expectation
    upper_latitude = abs(90 - x/2) 
    lower_latitude = abs(90 - x/2 + 0.5)
    area_of_latitude_band[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_latitude)) - np.sin(np.deg2rad(lower_latitude))))
    casualty_expectation[x] =  casualty_by_latitude[x] / area_of_latitude_band[x]

print('Sanity check: Earth area = ', sum(area_of_latitude_band))

np.savetxt(filename, casualty_expectation)
print("Total risk for", filename, "is", sum(casualty_expectation) )