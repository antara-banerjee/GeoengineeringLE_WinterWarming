'''
Plot year of emergence of trend under geoengineering. 

-Used for temperature in publication. 
-Emergence defined as year when signal-to-noise ratio of trend exceeds 2.
'''

# standard imports
import glob
import numpy as np
import xarray as xr

# user imports
import ensemble_functions
import plot_functions
import vartimeproc 

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = "TREFHT"

#********************************************************************************************************
# feedback runs
def calc_SNR():

   SNRs = []
   N = 20
   for endyear in range(2021,2096):
       print(endyear)
       members = []
       for i in range(1,N+1):
           ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0]
           vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=endyear, varcode=varcode)
           trend = vartimeobj.trend_lat_lon(season)
           members.append(trend)
       ensmean, ensstd = ensemble_functions.stats(members) 
       SNR = abs(ensmean) / (ensstd / np.sqrt(N-1))
       SNRs.append(SNR)
   
   dim = 'endyear'
   new_coord = range(2021,2096)
   func = lambda *x: np.stack(x, axis=-1)
   xSNR = xr.apply_ufunc(func, *SNRs,
                        output_core_dims=[[dim]],
                        join='outer',
                        dataset_fill_value=np.nan)
   xSNR[dim] = new_coord

   xSNR.to_netcdf('SNR_'+varcode+'_trend.nc')

   return

#********************************************************************************************************
def plot_ToE():

   dsSNR = xr.open_dataset('SNR_'+varcode+'_trend.nc')
   SNR = dsSNR['__xarray_dataarray_variable__'].sortby('endyear', ascending=False)
   npSNR = np.array(SNR.values)
   nplat = np.array(SNR.lat.values)
   nplon = np.array(SNR.lon.values)
   npendyear = np.array(SNR.endyear.values)
   ToE = np.full((nplat.shape[0], nplon.shape[0]), 2095)

   # scan reversed year order, break when significance drops below 2
   for ilat in range(len(nplat)):
      for ilon in range(len(nplon)):
         for iendyear in range(len(npendyear)): 
            if npSNR[ilat,ilon,iendyear]<2:
               ToE[ilat,ilon] = npendyear[iendyear]+1
               break 

   plot_functions.plot_ToE(ToE, nplat, nplon, '(b) Trend significance year', outdir+'ToE_TREFHT.png', 2020, 2095, 5,'year')

#********************************************************************************************************
# Comment in/out below to i) reate SNR netcdf (takes time) or ii) plot (quick)
#calc_SNR()
plot_ToE()

#********************************************************************************************************
# END
#********************************************************************************************************
