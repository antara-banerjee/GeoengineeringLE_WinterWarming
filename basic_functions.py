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

#********************************************************************************************************
def extract_var_dims(ncpath, varname='', **dims):

   # load netcdf file
   ncmod     = ncdf_att.get_ncmod(ncpath)

   # get raw field
   var, = ncdf_att.get_vars(ncmod, varname)

   # dimensions
   dimdict = {}
   if 'xlonname' in dims:
       lon, = ncdf_att.get_dims(ncmod, lonname=dims['xlonname'])
       dimdict['lon']= lon
   if 'xlatname' in dims:
       lat, = ncdf_att.get_dims(ncmod, latname=dims['xlatname'])
       dimdict['lat'] = lat
   if 'xhgtname' in dims:
       hgt, = ncdf_att.get_dims(ncmod, hgtname=dims['xhgtname'])
       dimdict['hgt'] = hgt
   if 'xtimname' in dims:
       tim, = ncdf_att.get_dims(ncmod, timname=dims['xtimname'])
       dimdict['tim'] = tim

   # shuffle in longitude if needed
   #if 'xlonname' in dims:
   #   if dimdict['lon'][0]==0:
   #      print("Shifting 180 degrees in longitude")
   #      oldlon = np.copy(lon)
   #      dimdict['lon'] = oldlon - 180
   #      rollby = np.where(oldlon==180)[0][0]
   #      var = np.roll(var, -rollby, axis=2)

   return (var, dimdict)

#********************************************************************************************************
def time_subset(invar, time0, tim1, tim2):

   itim1 = (tim1 - time0)*12
   itim2 = (tim2 - time0)*12+12+2
   var_tsub = invar[itim1:itim2]
   tsub = var_tsub.shape[0]
   nsubyrs = int(tsub/12)

   return (var_tsub, nsubyrs)

#********************************************************************************************************
def seasonal_mean(invar, invar_nyrs, time_mean):

    if time_mean=='monthly':
       v_tmean = invar
    elif time_mean=='clim_monthly':
       v_tmean = np.empty(12)
       for i in range(12):
          j = np.arange(i, invar_nyrs*12, 12)
          v_tmean[i] = np.mean(invar[j], axis=0, dtype=np.float64)
    else:
       v_tmean = np.empty([invar_nyrs])
       if time_mean=='annual':
          for i in range(invar_nyrs):
             jan = 12*i
             v_tmean[i] = np.mean(invar[jan:jan+12], axis=0, dtype=np.float64)
       else:
          startmon_dict = {'JJA':5,'DJF':11,'MAM':2,'SON':8,'NDJF':10,'D':11,'J':0,'F':1}
          len_season = len(time_mean)
          v_tmean = np.zeros([invar_nyrs])
          for i in range(invar_nyrs):
             startmon = 12*i+startmon_dict[time_mean]
             v_tmean[i] = np.mean(invar[startmon:startmon+len_season], axis=0, dtype=np.float64)

    return v_tmean

#********************************************************************************************************
def latitude_mean(invar, lat, llat, ulat):

   illat = np.where(lat>=llat)[0][0]
   iulat = np.where(lat>=ulat)[0][0]+1
   sublat = np.cos(lat[illat:iulat]*np.pi/180)

   area_mean = np.sum(invar[illat:iulat]*sublat)/np.sum(sublat)

   return area_mean

#********************************************************************************************************
