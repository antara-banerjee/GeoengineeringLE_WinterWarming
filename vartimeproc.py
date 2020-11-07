'''
Main classes to extract variables and perform time processing. 

Contains:
	VarTimeProc (general)
	PrecipTimeProc (precipitation only)
 	SSTTimeProc (calculates Nino3.4 index)
'''

from cftime import DatetimeNoLeap
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

#********************************************************************************************************
# The following class contains functions to select variable and process in time between tim1 and tim2
#********************************************************************************************************
class VarTimeProc:
    
   #**************************************************
   def __init__(self, ncpath, tim1, tim2, varcode, zm=False):
        
       self.tim1 = tim1
       self.tim2 = tim2

       # open as xarray dataset
       self.ncmod = xr.open_dataset(ncpath)
       self.var = self.ncmod[varcode]

       # modify time coordinate for CESM (1 month backwards)
       oldtime = self.var['time']
       newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
       newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
       self.var = self.var.assign_coords(time=newtime)

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       self.vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2)+'-02-01'))

       # if zonal mean 
       if zm:
          self.vtsub = self.vtsub.isel(lon=0)

       # fill in missing values
       self.vtsub= self.vtsub.fillna(0)

   #**************************************************
   # climatological, seasonal mean
   def clim_mean(self, time_mean):

       vclim = self.vtsub.groupby('time.season').mean('time').sel(season=time_mean)

       # checking this is the same
       #vyrmn = self.annual_mean(time_mean) 
       #vclim = vyrmn.mean('time') 

       return vclim 

   #**************************************************
   # yearly, seasonal means
   def annual_mean(self, time_mean):

       ASseas= {'DJF':'DEC',
                'MAM':'MAR',
                'JJA':'JUN',
                'SON':'SEP'}
       vseas = self.vtsub.sel(time=(self.vtsub['time.season']==time_mean)) # select based on boolean array
       vyrmn = vseas.resample(time='AS-'+ASseas[time_mean]).mean()

       return vyrmn

   #**************************************************
   # trend of lat-lon field (per 30 years) 
   def trend_lat_lon(self, time_mean):

       SCALER = 30.

       vyrmn = self.annual_mean(time_mean)

       x = range(vyrmn.values.shape[0])
       y = np.reshape(vyrmn.values,(vyrmn.values.shape[0],-1))
       coeffs = np.polyfit(x, y, 1)
       trends = (coeffs[0,:]*SCALER).reshape(vyrmn.values.shape[1], vyrmn.values.shape[2])
       xrtrends = xr.DataArray(trends,coords=[('lat',vyrmn['lat']),('lon',vyrmn['lon'])])

       return(xrtrends)
      
   #**************************************************
   # trend of lat-hgt field (per 30 years)
   def trend_lat_hgt(self, time_mean):

       SCALER = 30.

       vyrmn = self.annual_mean(time_mean) 

       x = range(vyrmn.values.shape[0])
       y = np.reshape(vyrmn.values,(vyrmn.values.shape[0],-1))
       coeffs = np.polyfit(x, y, 1)
       trends = (coeffs[0,:]*SCALER).reshape(vyrmn.values.shape[1], vyrmn.values.shape[2])
       xrtrends = xr.DataArray(trends,coords=[('level',vyrmn['level']),('lat',vyrmn['lat'])])

       return(xrtrends)

#********************************************************************************************************
# The PrecipTimeProc class inherits the VarTimeProc class but initializes for precipitation 
# (two input fields)
#********************************************************************************************************
class PrecipTimeProc(VarTimeProc):
    
   #**************************************************
   def __init__(self, ncpath1, ncpath2, tim1, tim2, ppt1, ppt2):
       
       mpersec_to_mmperday = 86400000.

       self.tim1 = tim1
       self.tim2 = tim2
       
       # open as xarray dataset
       self.ncmod1 = xr.open_dataset(ncpath1)
       self.ncmod2 = xr.open_dataset(ncpath2)
       var_ppt1 = self.ncmod1[ppt1]
       var_ppt2 = self.ncmod2[ppt2]
       self.var = (var_ppt1 + var_ppt2)*mpersec_to_mmperday

       # modify time coordinate for CESM (1 month backwards)
       oldtime = self.var['time']
       newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
       newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
       self.var = self.var.assign_coords(time=newtime)

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       self.vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2)+'-02-01'))

#********************************************************************************************************
# The SSTTimeProc inherits the VarTimeProc class but contains method to calculate Nino3.4 index 
#********************************************************************************************************
class SSTTimeProc(VarTimeProc):

   #**************************************************
   def __init__(self, ncpath, tim1, tim2, varcode):

      VarTimeProc.__init__(self, ncpath, tim1, tim2, varcode)

   #**************************************************
   def calc_n34(self):

      # monthly climatology
      sst_clim = self.var.groupby('time.month').mean(dim='time')
      
      # anomaly from monthly, climatological mean
      sst_anom = self.var.groupby('time.month') - sst_clim
      
      # compute ENSO index
      sst_anom_nino34 = sst_anom.sel(lat=slice(-5, 5), lon=slice(190, 240)) 
      sst_anom_nino34_mean = sst_anom_nino34.mean(dim=('lon', 'lat'))
      nino34 = sst_anom_nino34_mean.rolling(time=5).mean(dim='time')

      # write to file
      Ftime = open("time_feedback.txt","w")
      Ftime.write(str(nino34['time'].values))
      Ftime.close()

      # plot ENSO index 
      fig, ax = plt.subplots()
      plt.plot(nino34['time'], nino34, color='k') 
      ax.grid()

      plt.axhline(y=0, color='k')

      plt.fill_between(nino34['time'].values, y1=0, y2=nino34, where=nino34>0, color='r') 
      plt.fill_between(nino34['time'].values, y1=0, y2=nino34, where=nino34<0, color='b') 
      
      plt.savefig('nino34.png')

      return nino34

#********************************************************************************************************
# END
#********************************************************************************************************
     
