import glob
import numpy as np
import scipy.stats as ss
import netCDF4 as ncdf
import matplotlib as mpl
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
season = 'DJF'
outdir="/home/ab4283/scripts/glens/output/"
var = "PSL"
p_value = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

# control 
print "Calculating climatology for CONTROL"
members_control = []
for i in range(1,21):
   ncpath = glob.glob("/dx03/ab4283/GLENS/control/"+var+"/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   slp_inst = sea_level_pressure.slp(ncpath, time0=2010, tim1=2010, tim2=2030)
   clim_lon_lat = slp_inst.climatology_lon_lat(season)
   members_control.append(clim_lon_lat)
ensmean_control, ensstd_control, nens_control = ensemble_functions.calc_ensemble_mean(members_control)

# RCP8.5
# only 3 members here!
print "Calculating climatology for RCP8.5"
members_rcp85 = []
for i in range(1,4):
   ncpath = glob.glob("/dx03/ab4283/GLENS/control/"+var+"/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   slp_inst = sea_level_pressure.slp(ncpath, time0=2010, tim1=2075, tim2=2095)
   clim_lon_lat = slp_inst.climatology_lon_lat(season)
   members_rcp85.append(clim_lon_lat)
ensmean_rcp85, ensstd_rcp85, nens_rcp85 = ensemble_functions.calc_ensemble_mean(members_rcp85)

# feedback runs
print "Calculating climatology for FEEDBACK"
members_feedback = []
for i in range(1,21):
   ncpath = glob.glob("/dx03/ab4283/GLENS/feedback/"+var+"/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   slp_inst = sea_level_pressure.slp(ncpath, time0=2020, tim1=2075, tim2=2095)
   clim_lon_lat = slp_inst.climatology_lon_lat(season)
   members_feedback.append(clim_lon_lat)
ensmean_feedback, ensstd_feedback, nens_feedback = ensemble_functions.calc_ensemble_mean(members_feedback)

# differences
ensdiff_rcp85 = (ensmean_rcp85 - ensmean_control)/100.
ensdiff_feedback = (ensmean_feedback - ensmean_control)/100.

# two-tailed t-test
ttest_rcp85 = ensemble_functions.t_test(p_value, ensdiff_rcp85*100, ensstd_control, ensstd_rcp85, nens_control, nens_rcp85) 
ttest_feedback = ensemble_functions.t_test(p_value, ensdiff_feedback*100, ensstd_control, ensstd_feedback, nens_control, nens_feedback) 

# individual member differences
memdiff_feedback = map(lambda x: (x - ensmean_control)/100., members_feedback)
memdiff_rcp85 = map(lambda x: (x - ensmean_control)/100., members_rcp85)

# get lat and hgt off one instance 
lat = (slp_inst.dimdict)['lat']
lon = (slp_inst.dimdict)['lon']

#********************************************************************************************************
# Plot ensemble mean difference FEEDBACK-CONTROL

#print "Plotting ensemble mean difference FEEDBACK-CONTROL"
#ensemble_functions.plot_single_lat_lon(ensdiff_feedback, lat, lon, 'Feedback (2075-2095) - Control (2010-2030), '+season, outdir+'psl_ensdiff_feedback-control_'+season+'.png', 5, 1, 'SLP (hPa)', zsig=ttest_feedback)
#
#print "Plotting ensemble mean difference RCP8.5-CONTROL"
#ensemble_functions.plot_single_lat_lon(ensdiff_rcp85, lat, lon, 'RCP8.5 (2075-2095) - Control (2010-2030), '+season, outdir+'psl_ensdiff_rcp85-control_'+season+'.png', 5, 1, 'SLP (hPa)', zsig=ttest_rcp85)

print "Plotting member differences FEEDBACK-CONTROL"
ensemble_functions.plot_matrix_lat_lon(memdiff_feedback, lat, lon, 'Feedback (2075-2095) - Control (2010-2030), '+season, outdir+'psl_memdiff_feedback-control_'+season+'.pdf', 8, 1, 'SLP (hPa)')

print "Plotting member differences RCP8.5-CONTROL"
ensemble_functions.plot_matrix_lat_lon(memdiff_rcp85, lat, lon, 'RCP8.5 (2075-2095) - Control (2010-2030), '+season, outdir+'psl_memdiff_rcp85-control_'+season+'.pdf', 8, 1, 'SLP (hPa)')
#********************************************************************************************************
