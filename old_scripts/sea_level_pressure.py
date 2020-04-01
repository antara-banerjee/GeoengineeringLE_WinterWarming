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
import basic_functions

#********************************************************************************************************
class slp:
    
   def __init__(self, ncpath, time0, tim1, tim2):#, plev_unit='Pa', long_name=''):
        
       self.time0 = time0
       self.tim1 = tim1
       self.tim2 = tim2

       self.var, self.dimdict = basic_functions.extract_var_dims(ncpath, varname='PSL', xlonname='lon', xlatname='lat', xtimname='time')

       print(self.var.shape)

   #**************************************************
   def climatology_lon_lat(self, time_mean):

       # seasonal mean then average over climatological time period
       clim_var = np.zeros([len(self.dimdict['lat']),len(self.dimdict['lon'])])
       for ilat in range(len(self.dimdict['lat'])):
          for ilon in range(len(self.dimdict['lon'])):
             var_tsub, nsubyrs = basic_functions.time_subset(self.var[:,ilat,ilon], self.time0, self.tim1, self.tim2)
             var_seas = basic_functions.seasonal_mean(var_tsub, nsubyrs, time_mean)
             var_clim_seas = np.mean(var_seas, axis=0)
             clim_var[ilat,ilon] = var_clim_seas

       return clim_var

#********************************************************************************************************

   
