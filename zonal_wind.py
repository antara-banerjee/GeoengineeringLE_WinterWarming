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
class zmzw:

   def __init__(self, ncpath, time0, tim1, tim2):#, plev_unit='Pa', long_name=''):
        
       self.time0 = time0
       self.tim1 = tim1
       self.tim2 = tim2

       self.var, self.dimdict = basic_functions.extract_var_dims(ncpath, varname='U', xlatname='lat', xhgtname='lev', xtimname='time')

   #**************************************************
   def climatology_lat_hgt(self, time_mean):

       # seasonal mean then average over climatological time period
       clim_var = np.zeros([len(self.dimdict['hgt']),len(self.dimdict['lat'])])
       for ihgt in range(len(self.dimdict['hgt'])):
          for ilat in range(len(self.dimdict['lat'])):
             var_tsub, nsubyrs = basic_functions.time_subset(self.var[:,ihgt,ilat], self.time0, self.tim1, self.tim2)
             var_seas = basic_functions.seasonal_mean(var_tsub, nsubyrs, time_mean)
             var_clim_seas = np.mean(var_seas, axis=0)
             clim_var[ihgt,ilat] = var_clim_seas

       return clim_var

   #**************************************************
   def climatology_polar_hgt_mon(self):

       # polar cap mean (70-90N)
       var_amean = np.zeros([len(self.dimdict['tim']),len(self.dimdict['hgt'])])
       for itim in range(len(self.dimdict['tim'])):
          for ihgt in range(len(self.dimdict['hgt'])):
             var_amean[itim,ihgt] = basic_functions.latitude_mean(self.var[itim,ihgt,:], self.dimdict['lat'], 70, 90)

       # climatological monthly mean
       clim_var = np.zeros([12,len(self.dimdict['hgt'])])
       for ihgt in range(len(self.dimdict['hgt'])):
          var_tsub, nsubyrs = basic_functions.time_subset(var_amean[:,ihgt], self.time0, self.tim1, self.tim2)
          var_seas = basic_functions.seasonal_mean(var_tsub, nsubyrs, 'clim_monthly')
          clim_var[:,ihgt] = var_seas 
       
       return clim_var

   #**************************************************
   def climatology_shgt_slat(self, selhgt, sellat, time_mean):

       shgt = np.where(self.dimdict['hgt']>=selhgt)[0][0]
       slat = np.where(self.dimdict['lat']>=sellat)[0][0]

       # select variable at height and latitude  
       var = self.var[:,shgt,slat]

       # climatological monthly mean
       var_tsub, nsubyrs = basic_functions.time_subset(var, self.time0, self.tim1, self.tim2)
       var_seas = basic_functions.seasonal_mean(var_tsub, nsubyrs, time_mean)
       var_clim_seas = var_seas.mean()
       print var_clim_seas.shape
       
       return var_clim_seas 
# Calculate the lat-hgt climatology for control, geoengineering. Subtract.
# As above but with hgt-mon
#********************************************************************************************************

   
