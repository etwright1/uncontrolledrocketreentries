# Uncontrolled rocket reentries

This repository contains the data and code used in the paper 'Unnecessary risks created by uncontrolled rocket reentries' (2022) by Michael Byers, Ewan Wright, Aaron Boley, and Cameron Byers.

It is provided for independent assessment. If you use information provided here, please cite the 2022 paper.

The method of calculating weighting functions and casualty expectation is described in the main text of the paper.

Licence (CC BY-SA 4.0): https://creativecommons.org/licenses/by-sa/4.0/

# Data Sources

The Celestrak satellite catalogue was used, taken on 5 May 2022. http://celestrak.com/

Gridded Population of the World 4 datasets were used for population data for both 2020 and 2005, with half degree (55 km) latitude bins. Population counts are used, which are then converted to density values. https://sedac.ciesin.columbia.edu/data/collection/gpw-v4

Center for International Earth Science Information Network - CIESIN. Gridded Population of the World, Version 4.11 (GPWv4): UN WPP-Adjusted Population Count. Accessed 31 January (2022).

# Data values in text

The May 1992-2022 casualty expectation estimate is calculated using 'make_hist_wf_and_cas_exp.py'.

The casualty expectation corresponding to the 651 rocket bodies (RBs) with perigee < 600 km is found using 'find_casualty_risk.py'

The casualty expectation corresponding to a 10 year average weighting function is found using 'future_casualty_expectation.py'

# Plots

## Figure 1

The casualty expectation values for each state were calculated using in the 'find_casualty_risk' script. The RB inclinations for all 651 RBs and by each state used are in separate CSV files in the 'Input files' folder. These casualty expectations and RB counts were collated in a table for figure 1A.

The rest of figure 1 was created with the following scripts:

'plot_figure_1B'

'plot_figure_1C'

'plot_figure_1D'

## Figure 2

The weighting function from find_casualty_risk in figure 1 is used for the 'in orbit with perigee < 600' plot. The second weighting function was created using 'make_hist_wf_and_cas_exp' script.

'plot_figure_2' puts them both together.

## Figure 3

Figure 3 was created with 'make_heatmap_background',  which creates the file 'heatmap_image'. This is then cropped and the coastlines from Cartopy in the file 'coastlines_cropped_filtered' are then overlaid. This resulting heatmap is used as a background image in 'make_heatmap_overlay', which adds the population density line. The city labels and legend (from 'heatmap_image') are then added.

GIMP was used as image editor.
