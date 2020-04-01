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
import zonal_wind
import ensemble_functions

#********************************************************************************************************
season = 'DJF'
outdir="/home/ab4283/scripts/glens/output/"
var = "U"
p_value = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

# control 
print "Calculating climatology for CONTROL"
members_control = []
for i in range(1,21):
   if i in range(1,4):
      ncpath = "/dx03/ab4283/GLENS/control/"+var+"/zonal_mean_camelot/merged/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+var+".201001-209912.nc"
   else:
      ncpath = "/dx03/ab4283/GLENS/control/"+var+"/zonal_mean_camelot/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+var+".201001-203012.nc"
   zmzw_inst = zonal_wind.zmzw(ncpath, time0=2010, tim1=2010, tim2=2030)
   clim_lat_hgt = zmzw_inst.climatology_polar_hgt_mon()
   members_control.append(clim_lat_hgt)
ensmean_control, ensstd_control, nens_control= ensemble_functions.calc_ensemble_mean(members_control)

# RCP8.5
# only 3 members here!
print "Calculating climatology for RCP8.5"
members_rcp85 = []
for i in range(1,4):
   ncpath = "/dx03/ab4283/GLENS/control/"+var+"/zonal_mean_camelot/merged/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+var+".201001-209912.nc"
   zmzw_inst = zonal_wind.zmzw(ncpath, time0=2010, tim1=2075, tim2=2095)
   clim_lat_hgt = zmzw_inst.climatology_polar_hgt_mon()
   members_rcp85.append(clim_lat_hgt)
ensmean_rcp85, ensstd_rcp85, nens_rcp85 = ensemble_functions.calc_ensemble_mean(members_rcp85)

# feedback runs
print "Calculating climatology for FEEDBACK"
members_feedback = []
for i in range(1,21):
   ncpath = "/dx03/ab4283/GLENS/feedback/"+var+"/zonal_mean_camelot/merged/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0zm."+var+".202001-209912.nc"
   zmzw_inst = zonal_wind.zmzw(ncpath, time0=2020, tim1=2075, tim2=2095)
   clim_lat_hgt = zmzw_inst.climatology_polar_hgt_mon()
   members_feedback.append(clim_lat_hgt)
ensmean_feedback, ensstd_feedback, nens_feedback = ensemble_functions.calc_ensemble_mean(members_feedback)

# differences
ensdiff_rcp85 = ensmean_rcp85 - ensmean_control
ensdiff_feedback = ensmean_feedback - ensmean_control

# two-tailed t-test
ttest_rcp85 = ensemble_functions.t_test(p_value, ensdiff_rcp85, ensstd_control, ensstd_rcp85, nens_control, nens_rcp85) 
ttest_feedback = ensemble_functions.t_test(p_value, ensdiff_feedback, ensstd_control, ensstd_feedback, nens_control, nens_feedback) 

print 'DIFF SHAPE ', ensdiff_feedback.shape

# individual member differences
memdiff_feedback = map(lambda x: x - ensmean_control, members_feedback)
memdiff_rcp85 = map(lambda x: x - ensmean_control, members_rcp85)

# get hgt off one instance 
hgt = (zmzw_inst.dimdict)['hgt']

#********************************************************************************************************
# Plot ensemble mean difference FEEDBACK-CONTROL
#print "Plotting ensemble mean difference FEEDBACK-CONTROL"
#ensemble_functions.plot_single_hgt_mon(ensdiff_feedback, ensmean_control, hgt, 'Feedback (2075-2095) - Control (2010-2030)\n'+season, outdir+'U_monthly_ensdiff_feedback-control_'+season+'.png', 8, 1, 40, 5, r'U (ms$^{-1}$)', colorbar=True, zsig=ttest_feedback)
#
## Plot ensemble mean difference RCP8.5-CONTROL
#print "Plotting ensemble mean difference RCP8.5-CONTROL"
#ensemble_functions.plot_single_hgt_mon(ensdiff_rcp85, ensmean_control, hgt, 'RCP8.5 (2075-2095) - Control (2010-2030)\n'+season, outdir+'U_monthly_ensdiff_rcp85-control_'+season+'.png', 8, 1, 40, 5, r'U (ms$^{-1}$)', colorbar=True, zsig=ttest_rcp85)

print "Plotting member differences FEEDBACK-CONTROL"
ensemble_functions.plot_matrix_hgt_mon(memdiff_feedback, ensmean_control, hgt, 'Feedback (2075-2095) - Control (2010-2030), '+season, outdir+'U_monthly_memdiff_feedback-control_'+season+'.pdf', 8, 1, 40, 5, r'U (ms$^{-1}$)')

print "Plotting member differences RCP8.5-CONTROL"
ensemble_functions.plot_matrix_hgt_mon(memdiff_rcp85, ensmean_control, hgt, 'RCP8.5 (2075-2095) - Control (2010-2030), '+season, outdir+'U_monthly_memdiff_rcp85-control_'+season+'.pdf', 8, 1, 40, 5, r'U (ms$^{-1}$)')
##********************************************************************************************************
#paths_feedback = []
#for i in range(1,21):
#   for j in range(2,10): 
#      ncpath = "/dx03/ab4283/GLENS/feedback/U/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.U.20"+str(j)+"001-20"+str(j)+"912.nc"
#      lon, lat, var_block = zonal_wind.extract_var(ncpath, xlonname='lon', xlatname='lat', xtimname='time', varname='U')
#      print var_block.shape
#   #var_tseries = 
#   #var_feedback.append(var_tseries)
