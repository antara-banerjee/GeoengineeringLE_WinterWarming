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
class Ts:
    
   def __init__(self, ncpath, time0, tim1, tim2, varname):#, plev_unit='Pa', long_name=''):
        
       self.time0 = time0
       self.tim1 = tim1
       self.tim2 = tim2

       self.var, self.dimdict = basic_functions.extract_var_dims(ncpath, varname=varname, xlonname='lon', xlatname='lat', xtimname='time')

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

   #**************************************************
   def region_mean(self, invar, lon0, lon1, lat0, lat1):

      ilon0 = np.where(self.dimdict['lon']>=lon0)[0][0]
      ilon1 = np.where(self.dimdict['lon']>=lon1)[0][0]
      ilat0 = np.where(self.dimdict['lat']>=lat0)[0][0]
      ilat1 = np.where(self.dimdict['lat']>=lat1)[0][0]

      invar_amean = np.mean(invar[ilon0:ilon1+1,ilat0:ilat1+1])

      return invar_amean

#********************************************************************************************************
class sst(Ts):

   def __init__(self, ncpath, time0, tim1, tim2, varname):

      Ts.__init__(self, ncpath, time0, tim1, tim2, varname)

      #self.var = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

   def calc_n34(self):

      #print('got to function')
      vtsub, nyrs = basic_functions.time_subset(self.var, self.time0, self.tim1, self.tim2)

      # Compute monthly climatology    
      sst_clim = np.zeros([12,len(self.dimdict['lat']),len(self.dimdict['lon'])])
      for i in range(12):
         j = np.arange(i,nyrs*12,12)
         sst_clim[i,:,:] = np.mean(vtsub[j,:,:], axis=0)

      # Compute anomaly
      sst_anom = np.zeros([vtsub.shape[0], vtsub.shape[1], vtsub.shape[2]])
      for i in range(vtsub.shape[0]):
         j = i%12; print(j)
         sst_anom[i,:,:] = vtsub[i,:,:] - sst_clim[j,:,:] 

      # Area mean
      illat = np.where(self.dimdict['lat']>=-5)[0][0]
      iulat = np.where(self.dimdict['lat']>=5)[0][0]+1
      illon = np.where(self.dimdict['lon']>=-170)[0][0]
      iulon = np.where(self.dimdict['lon']>=-120)[0][0]+1

      sst_anom_nino34 = np.mean(sst_anom[:, illat:iulat, illon:iulon], axis=(1,2)) # should weight latitude

      # 5-month running mean
      smooth_length = 5
      x = (smooth_length-1)/2
      nino34  = np.zeros([sst_anom_nino34.shape[0]-smooth_length+1])
      #time = range(nyrs*12)
      t = []
      for i in range(sst_anom_nino34.shape[0]-smooth_length+1):
          nino34[i] = np.mean(sst_anom_nino34[i:i+smooth_length])
          t.append(x+i)
          #years.append(self.tim1+x+i)

      fig, ax = plt.subplots();
      plt.plot(t, nino34, color='k')
      ax.grid();

      plt.axhline(y=0, color='k')

      plt.fill_between(t, y1=0, y2=nino34, where=nino34>0, color='r')
      plt.fill_between(t, y1=0, y2=nino34, where=nino34<0, color='b')

      plt.savefig('nino34_numpy.png')

      '''
      # Computed climatology
      sst_clim = self.var.groupby('time.month').mean(dim='time')

      # Compute Anomaly
      sst_anom = self.var.groupby('time.month') - sst_clim

      # Compute ENSO index
      sst_anom_nino34 = sst_anom.sel(lat=slice(-5, 5), lon=slice(190, 240))

      sst_anom_nino34_mean = sst_anom_nino34.mean(dim=('lon', 'lat'))

      nino34 = sst_anom_nino34_mean.rolling(time=5).mean(dim='time')
      Fn34 = open("nino34_feedback_001.txt","w")
      Ftime = open("time_feedback_001.txt","w")
      Fn34.write(str(list(nino34.values)))
      Ftime.write(str(nino34['time'].values))
      Fn34.close()
      Ftime.close()
      print(list(nino34.values))
      print(nino34['time'].values)
      '''
      
#********************************************************************************************************

   
