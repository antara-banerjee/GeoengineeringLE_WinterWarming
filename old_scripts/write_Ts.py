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
import surface_temp
import ensemble_functions

#********************************************************************************************************
season = 'SON'
outdir="/home/ab4283/scripts/glens/output/"
var = "TREFHT"
p_value = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

# control 
print("Calculating climatology for CONTROL")
members_control = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2010, tim1=2010, tim2=2030)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_control.append(clim_lon_lat)
print(np.array(members_control).shape)
np.save("nparrays/"+var+"_control_"+season, np.array(members_control))
ensmean_control, ensstd_control, nens_control = ensemble_functions.calc_ensemble_mean(members_control)

# RCP8.5
# only 3 members here!
print("Calculating climatology for RCP8.5")
members_rcp85 = []
for i in [1,2,3,21]:
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2010, tim1=2075, tim2=2095)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_rcp85.append(clim_lon_lat)
print(np.array(members_rcp85).shape)
np.save("nparrays/"+var+"_rcp85_"+season, np.array(members_rcp85))
ensmean_rcp85, ensstd_rcp85, nens_rcp85 = ensemble_functions.calc_ensemble_mean(members_rcp85)

# feedback runs
print("Calculating climatology for FEEDBACK")
members_feedback = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2020, tim1=2075, tim2=2095)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_feedback.append(clim_lon_lat)
print(np.array(members_feedback).shape)
np.save("nparrays/"+var+"_feedback_"+season, np.array(members_feedback))
ensmean_feedback, ensstd_feedback, nens_feedback = ensemble_functions.calc_ensemble_mean(members_feedback)

# save dimensions
# get lat and hgt off one instance 
#lat = (Ts_inst.dimdict)['lat']
#lon = (Ts_inst.dimdict)['lon']
#np.save("nparrays/GLENS_lat", np.array(lat))
#np.save("nparrays/GLENS_lon", np.array(lon))
