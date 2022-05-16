# 
# Code for analysing rocket body reentries
# by etwright1 (E. Wright), 2022
#

import numpy as np

RE=6378000 # equatorial radius in m

thirty_year_weighting_function = np.genfromtxt("Output data/rb decayed 1992-2021 7 days_weighting function.csv", delimiter=' ') # 1991-2021 weighting function
ten_year_weighting_function = thirty_year_weighting_function / 3
latitudes = list(reversed(np.arange(-90, 90, 0.5)))

population_2020 = np.genfromtxt("Input data/GPW4_2020.csv", delimiter=' ') # import and clean GPW4 population data
population_2020 = np.where(population_2020==-9999, 0, population_2020) 

print(f'sensecheck: population in 2020 = {np.sum(population_2020)}')

future_years = 7 # we want to find the 2027 population to multiple by the 10 year wf. We are modelling 2022-2031 inclusive

population_sums = []
future_populations = []
average_population_growth_rate = 0.01 # 1% annual population growth rate assumed

# Modelling the population each year and multiplying it by a yearly weighting function is equivalent to modelling the 2027 population
# and multiplying it by a 10 year weighting function. 

for i in np.arange(1,future_years+1,1):
    year_population = population_2020*(1 + average_population_growth_rate)**i # modelling growth per year#
    future_populations.append(year_population) 
    population_sums.append(np.sum(year_population)) # populations from 2021-2027

print(f'Sense check: population in 2027 = {np.sum(future_populations[6])}')

population_2027 = future_populations[6]
grid = np.ones((360,720))

for x in range(720):
    grid[:,x] = population_2027[:,x] * ten_year_weighting_function # Two dimensional, this is a slightly convoluted method
casualty_by_latitude = grid.sum(axis=1) # back to one dimension

area_of_latitude_band = np.ones(len(latitudes))
casualty_expectation = np.ones(len(latitudes))

for x in range(len(latitudes)): # dividing by area to get casualty expectation
    upper_latitude = abs(90 - x/2) 
    lower_latitude = abs(90 - x/2 + 0.5)
    area_of_latitude_band[x] = 2 * np.pi * RE**2 * abs((np.sin(np.deg2rad(upper_latitude)) - np.sin(np.deg2rad(lower_latitude))))
    casualty_expectation[x] =  casualty_by_latitude[x] / area_of_latitude_band[x]

np.savetxt('Output data/future_casualty_expectation.csv', casualty_expectation)

print(f'The total casualty expectation value is {np.sum(casualty_expectation)}')
