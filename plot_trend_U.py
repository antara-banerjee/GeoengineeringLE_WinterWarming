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
import zonal_wind
import ensemble_functions

#********************************************************************************************************
season = 'DJF'
outdir="/home/ab4283/scripts/glens/output/"
var = "U"
alpha = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

#********************************************************************************************************
# RCP8.5
# only 3 members here!
print("Calculating climatology for RCP8.5")

members_rcp85 = []
for i in [1,2,3,21]:
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   U_inst = zonal_wind.zmzw(ncpath, tim1=2020, tim2=2095, var='U')
   trend_lon_lat = U_inst.trend(season)
   members_rcp85.append(trend_lon_lat)

nrcp85 = len(members_rcp85)
ensmean_rcp85, ensstd_rcp85 = ensemble_functions.stats(members_rcp85)
ttest_rcp85 = ensemble_functions.t_test_onesample(alpha, ensmean_rcp85, ensstd_rcp85, nrcp85) 

plot_functions.plot_single_lat_lon(ensmean_rcp85, 'RCP8.5 ('+season+')', outdir+'U_trend_rcp85_'+season+'.png', 8, 1, 40, 5, '$^{\circ}$C per 30 yrs', zsig=ttest_rcp85)

#********************************************************************************************************
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   U_inst = zonal_wind.zmzw(ncpath, tim1=2020, tim2=2095, var='U')
   trend_lon_lat = U_inst.trend_lon_lat(season)
   members_feedback.append(trend_lon_lat)

nfeedback = len(members_feedback)
ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback)
ttest_feedback = ensemble_functions.t_test_onesample(alpha, ensmean_feedback, ensstd_feedback, nfeedback) 

plot_functions.plot_single_lat_lon(ensmean_feedback, 'Feedback ('+season+')', outdir+'U_trend_feedback_'+season+'.png', 8, 1, 40, 5, '$^{\circ}$C per 30 yrs', zsig=ttest_feedback)
#********************************************************************************************************

##********************************************************************************************************
#paths_feedback = []
#for i in range(1,21):
#   for j in range(2,10): 
#      ncpath = "/dx03/ab4283/GLENS/feedback/U/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.U.20"+str(j)+"001-20"+str(j)+"912.nc"
#      lon, lat, var_block = zonal_wind.extract_var(ncpath, xlonname='lon', xlatname='lat', xtimname='time', varname='U')
#      print var_block.shape
#   #var_tseries = 
#   #var_feedback.append(var_tseries)
