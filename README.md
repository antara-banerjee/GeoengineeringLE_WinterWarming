# Geoengineering Large ENSemble (GLENS) winter warming analysis

## Introduction
This code accompanies the publication: https://acp.copernicus.org/preprints/acp-2020-965/. It analyzes climate changes over Eurasia in output from the GLENS 
ensemble of simulations performed at NCAR with the CESM-WACCM global chemistry-climate model. In particular, the role of stratospheric dynamical changes in 
leading to the surface climate responses is quantified using a combination of EOF/PCA - to calculate the Northern Annular Mode (NAM) and North Atlantic Oscillation 
(NAO) - and linear regression.

## Key modules
vartimeproc: classes for extraction and time processing of variables from netcdf files

clim_defs: functions to calculate climatologies in GLENS

ensemble_functions: functions to calculate ensemble statistics (mean, standard deviation, t-statistics)

trend_defs: functions to calculate trends in GLENS

PCA_defs: functions to calculate EOFs/PCs

plot_defs: plotting functions

## Data sources
The GLENS data are publicly available via the Earth System Grid: www.cesm.ucar.edu/projects/community-projects/GLENS/
(doi:/10.5065/D6JH3JXX). 
