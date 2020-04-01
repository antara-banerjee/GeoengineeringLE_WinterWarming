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
import plot_functions

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
var = "TS"

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

#********************************************************************************************************
# RCP8.5
# only 3 members here!
print("Calculating climatology for RCP8.5")

members_rcp85 = []
for i in [1]:
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   SST_inst = surface_temp.sst(ncpath, time0=2010, tim1=2020, tim2=2095, var=var)
   n34 = SST_inst.calc_n34()
   members_rcp85.append(n34)

print("...done")

##********************************************************************************************************
## feedback runs
#print("Calculating climatology for FEEDBACK")
#
#members_feedback = []
#for i in range(1,2):
#   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
#   SST_inst = surface_temp.sst(ncpath, time0=2020, tim1=2020, tim2=2095, var=var)
#   n34 = SST_inst.calc_n34()
#   members_feedback.append(n34)
#
#print("...done")
#********************************************************************************************************
