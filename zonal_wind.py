import numpy as np
import xarray as xr
from cftime import DatetimeNoLeap

#********************************************************************************************************
class zmzw:

   def __init__(self, ncpath='', tim1='', tim2='', var=''):
        
       self.tim1 = tim1
       self.tim2 = tim2

       # open as xarray dataset
       self.ncmod = xr.open_dataset(ncpath)
       self.var = self.ncmod[var]

       # zonal mean - choose single longitude 
       self.var = self.var.isel(lon=0)

       # modify time coordinate for CESM (1 month backwards)
       oldtime = self.var['time']
       newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
       newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
       self.var = self.var.assign_coords(time=newtime)

       self.var = self.var.fillna(0)

       self.trend_scaling = 30.

   #**************************************************
   # climatological mean
   def climatology_lon_lat(self, time_mean):

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

       # climatological, seasonal mean
       vseas = vtsub.groupby('time.season').mean('time').sel(season=time_mean)

       return vseas

   '''
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
   '''

   #**************************************************
   # trend
   def trend_lon_lat(self, time_mean):

       # time subset
       # this subsetting allows for DJF mean that includes only D of the firt year and JF of the last year plus one
       vtsub = self.var.sel(time=slice(str(self.tim1)+'-03-01', str(self.tim2+1)+'-02-01'))

       # annual, seasonal mean - pandas gives me RAGE
       ASseas= {'DJF':'AS-DEC',
                'MAM':'AS-MAR',
                'JJA':'AS-JUN',
                'SON':'AS-SEP'}
       vseas = vtsub.sel(time=(vtsub['time.season']==time_mean)) # select based on boolean array
       vyrmn = vseas.resample(time=ASseas[time_mean]).mean()

       x = range(vyrmn.values.shape[0])
       y = np.reshape(vyrmn.values,(vyrmn.values.shape[0],-1))
       coeffs = np.polyfit(x, y, 1)
       trends = (coeffs[0,:]*self.trend_scaling).reshape(vyrmn.values.shape[1], vyrmn.values.shape[2])
       xrtrends = xr.DataArray(trends,coords=[('level',vyrmn['level']),('lat',vyrmn['lat'])])
       print(xrtrends)

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

#********************************************************************************************************

   
