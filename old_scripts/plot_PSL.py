import glob
import numpy as np
import scipy.stats as ss
import netCDF4 as ncdf
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
#plt.ioff()
import calendar
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
from matplotlib.backends.backend_pdf import PdfPages
# mpl_toolkits contain the class Basemap and other functions such
# as addcyclic, shiftgrid etc.
from pylab import *
import matplotlib.cm as cm
import matplotlib.colors as colors
import custom_colors as ccol
import numpy.ma as ma
import get_netcdf_attributes as ncdf_att
import sea_level_pressure
import ensemble_functions

#********************************************************************************************************
season = 'SON'
outdir="/Users/abanerjee/scripts/glens/output/"
var = "PSL"
p_value = 0.05

#********************************************************************************************************
# load data
members_control = np.load("nparrays/"+var+"_control_"+season+".npy")[:-1]
members_rcp85 = np.load("nparrays/"+var+"_rcp85_"+season+".npy")[:-1]
members_feedback = np.load("nparrays/"+var+"_feedback_"+season+".npy")[:-1]
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

ensmean_control, ensstd_control, nens_control = ensemble_functions.calc_ensemble_mean(members_control)
ensmean_rcp85, ensstd_rcp85, nens_rcp85 = ensemble_functions.calc_ensemble_mean(members_rcp85)
ensmean_feedback, ensstd_feedback, nens_feedback = ensemble_functions.calc_ensemble_mean(members_feedback)

# differences
ensdiff_rcp85 = (ensmean_rcp85 - ensmean_control)/100.
ensdiff_feedback = (ensmean_feedback - ensmean_control)/100.

# two-tailed t-test
ttest_rcp85 = ensemble_functions.t_test(p_value, ensdiff_rcp85*100, ensstd_control, ensstd_rcp85, nens_control, nens_rcp85) 
ttest_feedback = ensemble_functions.t_test(p_value, ensdiff_feedback*100, ensstd_control, ensstd_feedback, nens_control, nens_feedback) 

# individual member differences
memdiff_feedback = [(x - ensmean_control)/100. for x in members_feedback]
memdiff_rcp85 = [(x - ensmean_control)/100. for x in members_rcp85]

# get lat and hgt off one instance 
lat = np.load("nparrays/GLENS_lat.npy") 
lon = np.load("nparrays/GLENS_lon.npy") 

#********************************************************************************************************
# Plot ensemble mean difference FEEDBACK-CONTROL

print("Plotting ensemble mean difference FEEDBACK-CONTROL")
ensemble_functions.plot_single_lat_lon(ensdiff_feedback, lat, lon, 'Feedback (2075-2095) - Control (2010-2030)\n'+season, outdir+'psl_ensdiff_feedback-control_'+season+'.png', 5, 1, 'SLP (hPa)', zsig=ttest_feedback)

print("Plotting ensemble mean difference RCP8.5-CONTROL")
ensemble_functions.plot_single_lat_lon(ensdiff_rcp85, lat, lon, 'RCP8.5 (2075-2095) - Control (2010-2030)\n'+season, outdir+'psl_ensdiff_rcp85-control_'+season+'.png', 5, 1, 'SLP (hPa)', zsig=ttest_rcp85)

#print "Plotting member differences FEEDBACK-CONTROL"
#ensemble_functions.plot_matrix_lat_lon(memdiff_feedback, lat, lon, 'Feedback (2075-2095) - Control (2010-2030), '+season, outdir+'slp_memdiff_feedback-control_'+season+'.pdf', 8, 1, 'SLP (hPa)')
#
#print "Plotting member differences RCP8.5-CONTROL"
#ensemble_functions.plot_matrix_lat_lon(memdiff_rcp85, lat, lon, 'RCP8.5 (2075-2095) - Control (2010-2030), '+season, outdir+'slp_memdiff_rcp85-control_'+season+'.pdf', 8, 1, 'SLP (hPa)')
#********************************************************************************************************
