import numpy as np
import xarray as xr
from cftime import DatetimeNoLeap
import matplotlib.pyplot as plt

#********************************************************************************************************
# The following class contains function to calculate the climatology or the trend (per decade) between tim1 and tim2
class Ts:
    
   def __init__(self, ncpath='', tim1='', tim2='', var=''):
        
       self.tim1 = tim1
       self.tim2 = tim2

       # open as xarray dataset
       self.ncmod = xr.open_dataset(ncpath)
       self.var = self.ncmod[var]

       # modify time coordinate for CESM (1 month backwards)
       oldtime = self.var['time']
       newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
       newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
       self.var = self.var.assign_coords(time=newtime)
       #self.var, self.dimdict = basic_functions.extract_var_dims(ncpath, varname='TREFHT', xlonname='lon', xlatname='lat', xtimname='time')
       #self.var = self.var.isel(lat=slice(0,2), lon=slice(0,2))

       yr_to_dec = 10

   #**************************************************
   # climatological mean
   def climatology_lon_lat(self, time_mean):

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

       # climatological, seasonal mean
       vseas = vtsub.groupby('time.season').mean('time').sel(season=time_mean)

       return vseas

   #**************************************************
   # climatological mean
   def annual_lon_lat(self, time_mean):

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

       # annual, seasonal mean - pandas gives me RAGE
       ASseas= {'DJF':'DEC',
                'MAM':'MAR',
                'JJA':'JUN',
                'SON':'SEP'}
       vseas = vtsub.sel(time=(vtsub['time.season']==time_mean)) # select based on boolean array
       vyrmn = vseas.resample(time='AS-'+ASseas[time_mean]).mean()

       return vyrmn
   #**************************************************
   # trend
   def trend_lon_lat(self, time_mean):

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

       # annual, seasonal mean - pandas gives me RAGE
       ASseas= {'DJF':'DEC',
                'MAM':'MAR',
                'JJA':'JUN',
                'SON':'SEP'}
       vseas = vtsub.sel(time=(vtsub['time.season']==time_mean)) # select based on boolean array
       vyrmn = vseas.resample(time='AS-'+ASseas[time_mean]).mean()

       x = range(vyrmn.values.shape[0])
       y = np.reshape(vyrmn.values,(vyrmn.values.shape[0],-1))
       coeffs = np.polyfit(x, y, 1)
       trends = (coeffs[0,:]*30.).reshape(vyrmn.values.shape[1], vyrmn.values.shape[2])
       xrtrends = xr.DataArray(trends,coords=[('lat',vyrmn['lat']),('lon',vyrmn['lon'])])
       #print(xrtrends)

       ## trend
       #def ols_trend(xrobject):

       #   x = range(vseas.values.shape[0])
       #   y = np.reshape(vseas.values,(vseas.values.shape[0],-1))
       #   coeffs = np.polyfit(x, y, 1)
       #   trends = (coeffs[0,:]/30.).reshape(vseas.values.shape[1], vseas.values.shape[2])

       #dim = 'member'
       #new_coord = range(len(xrobjects))

       #func = lambda *x: np.stack(x, axis=-1)
       #stack = xr.apply_ufunc(func, *xrobjects,
       #                     output_core_dims=[[dim]],
       #                     join='outer',
       #                     dataset_fill_value=np.nan)

       #ensmean = stack.mean('member')
       #ensstd = stack.std('member')

       return(xrtrends)

   #**************************************************
   def region_mean(self, invar, lon0, lon1, lat0, lat1):

      ilon0 = np.where(self.dimdict['lon']>=lon0)[0][0]
      ilon1 = np.where(self.dimdict['lon']>=lon1)[0][0]
      ilat0 = np.where(self.dimdict['lat']>=lat0)[0][0]
      ilat1 = np.where(self.dimdict['lat']>=lat1)[0][0]

      invar_amean = np.mean(invar[ilon0:ilon1+1,ilat0:ilat1+1])

      return invar_amean
      
#********************************************************************************************************
class ppt(Ts):
    
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
        #self.var, self.dimdict = basic_functions.extract_var_dims(ncpath, varname='TREFHT', xlonname='lon', xlatname='lat', xtimname='time')
  
            
#********************************************************************************************************
            
class sst(Ts):

   def __init__(self, ncpath, tim1, tim2, var):

      Ts.__init__(self, ncpath, tim1, tim2, var)

      #self.var = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

   def calc_n34(self):

      # Computed climatology
      sst_clim = self.var.groupby('time.month').mean(dim='time')
      
      # Compute Anomaly
      sst_anom = self.var.groupby('time.month') - sst_clim
      
      # Compute ENSO index
      sst_anom_nino34 = sst_anom.sel(lat=slice(-5, 5), lon=slice(190, 240)) 
      
      sst_anom_nino34_mean = sst_anom_nino34.mean(dim=('lon', 'lat'))

      nino34 = sst_anom_nino34_mean.rolling(time=5).mean(dim='time')

      Ftime = open("time_feedback.txt","w")
      Ftime.write(str(nino34['time'].values))
      Ftime.close()

      # Plot the ENSO index 
      fig, ax = plt.subplots();
      x = range(len(nino34['time']))
      #nino34.plot(ax=ax, label='smoothed', color='k');
      plt.plot(nino34['time'], nino34, color='k') 
      ax.grid();

      plt.axhline(y=0, color='k')

      plt.fill_between(nino34['time'].values, y1=0, y2=nino34, where=nino34>0, color='r') 
      plt.fill_between(nino34['time'].values, y1=0, y2=nino34, where=nino34<0, color='b') 
      
      ## create a categorical  dataarray
      #anino34 = xr.full_like(nino34, 'none', dtype='U4')
      #anino34[nino34 >= 0.5] = 'nino'
      #anino34[nino34 <= -0.5] = 'nina'
      #print(anino34)
      #
      #sst_nino_composite = sst_anom.groupby(anino34.rename('anino34')).mean(dim='time')
      #print(sst_nino_composite)
      #
      #sst_nino_composite.plot(col='anino34');
      plt.savefig('nino34.png')

      return(nino34)
      #

     
