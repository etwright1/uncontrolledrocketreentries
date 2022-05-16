# Uncontrolled rocket reentries

This repository contains the data and code used in the paper 'Unnecessary risks created by uncontrolled rocket reentries', Nature Astronomy, Analysis (2022) by Michael Byers, Ewan Wright, Aaron Boley, and Cameron Byers.

It is provided for independent assessment. If you use information provided here, please cite the 2022 paper (LINK FORTHCOMING).

The method of calculating weighting functions and casualty expectation is described in the main text of the paper.

Licence (CC BY-SA 4.0): https://creativecommons.org/licenses/by-sa/4.0/

# Data Sources

The Celestrak satellite catalogue is used, taken on 5 May 2022. http://celestrak.com/

Gridded Population of the World 4 datasets are used for population data for both 2020 and 2005, with half degree (55 km) latitude bins. Population counts are used, which are then converted to density values. 

Center for International Earth Science Information Network - CIESIN. Gridded Population of the World, Version 4.11 (GPWv4): UN WPP-Adjusted Population Count. Accessed 31 January (2022). At: https://sedac.ciesin.columbia.edu/data/collection/gpw-v4

# Data values in text

The May 1992-2022 casualty expectation estimate is calculated using 'make_hist_wf_and_cas_exp.py'.

The casualty expectation corresponding to the 651 rocket bodies (RBs) with perigee < 600 km is found using 'find_casualty_risk.py'

The casualty expectation corresponding to a 10 year average weighting function is found using 'future_casualty_expectation.py'

# Plots

## Figure 1

The casualty expectation values for each state are calculated using the 'find_casualty_risk' script. The RB inclinations used in the study for all 651 RBs are in CSV files in the 'Input files' folder. The data are further separated into CSV files by their launching state. These casualty expectations and RB counts are collated in a Table for Figure 1A.

The rest of Figure 1 is created with the following scripts:

'plot_figure_1B'

'plot_figure_1C'

'plot_figure_1D'

## Figure 2

The weighting function from find_casualty_risk in Figure 1 is used for the 'in orbit with perigee < 600' plot. The second weighting function is created using 'make_hist_wf_and_cas_exp' script.

'plot_figure_2' puts the results from these scripts together.

## Figure 3

Figure 3 is created with 'make_heatmap_background',  which creates the file 'heatmap_image'. This is then cropped, and the coastlines from Cartopy in the file 'coastlines_cropped_filtered' are overlaid. This resulting heatmap is used as a background image in 'make_heatmap_overlay', which adds the population density line. The city labels and legend (from 'heatmap_image') are then added.

GIMP was used as an image editor for final presentation.
