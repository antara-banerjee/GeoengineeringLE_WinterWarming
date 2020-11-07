'''
Common definitions for EOF and PC extraction. 
Set up for NAM and NAO modes. 
Set up for seasonal means (DJF, MAM, JJA, SON).
'''

# standard imports
import cartopy.crs as ccrs
from cftime import DatetimeNoLeap
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA
import scipy.stats as ss
import xarray as xr

# third-party imports
from eofs.standard import Eof

#*********************************************************************************
# Pre-process file: extract variable, adjust time and longitude values
def preprocess(filename, varcode, tim1, tim2, vertical=False):

   # extract variable  
   var = xr.open_dataset(filename)[varcode] 

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset - start in March, end in February
   var = var.sel(time=slice(str(tim1)+'-03-01', str(tim2)+'-02-01'))

   # Adjust lon values to make sure they are within (-180, 180)
   lon_name = 'lon'  

   var['_longitude_adjusted'] = xr.where(
   var[lon_name] > 180,
   var[lon_name] - 360,
   var[lon_name])

   # reassign the new coords to as the main lon coords
   # and sort DataArray using new coordinate values
   var = (var 
      .swap_dims({lon_name: '_longitude_adjusted'})
      .sel(**{'_longitude_adjusted': sorted(var._longitude_adjusted)})
      .drop(lon_name))

   var = var.rename({'_longitude_adjusted': lon_name})

   # latitude subset
   #var = var.sel(lat=slice(20,80), lon=slice(-90,40))

   # convert variable and dimensions to numpy arrays 
   npvar = var.values
   nptime = var['time'].values
   nplat = var['lat'].values
   nplon = var['lon'].values
   if vertical:
      nplev = var['level'].values

   # for cos latitude weighting later
   coslat = np.cos(np.deg2rad(nplat))

   return (npvar, nptime, nplev, nplat, nplon, coslat) if vertical else (npvar, nptime, nplat, nplon, coslat)

#*********************************************************************************
# Remove global mean 
def remove_gm(var, lats, coslat):

   coslatarray = coslat[np.newaxis,:,np.newaxis]
   gm = np.nansum(var*coslatarray, axis=1)/np.sum(coslatarray)
   vargm = var - gm[:,np.newaxis,:]

   return vargm 

#*********************************************************************************
# Remove given monthly climatology and take seasonal mean
def calc_anom(var, monclim, season):

   startmonth = {'DJF':9,'MAM':0,'JJA':3,'SON':6}
   istartmonth = startmonth[season]

   # remove monthly climatology
   varDS = np.empty_like(var)
   for i in range(var.shape[0]):
      j = i%12
      varDS[i,...] = var[i,...] - monclim[j,...] 
   
   # seasonal mean
   nyrs = int(varDS.shape[0]/12)
   print('nyrs = ',nyrs)
   varSEAS = np.empty([nyrs, var.shape[1], var.shape[2]])
   for i in range(nyrs):
      j = istartmonth+(12*i) 
      varSEAS[i,...] = varDS[j:j+3,...].mean(axis=0)

   return varSEAS
   
#*********************************************************************************
# subset over NAM/NAO region
def area_subset(var, mode, lats, lons, coslat):

   if mode=='NAM':
      llat = 20
      ulat = lats[-1]
      llon = lons[0]
      ulon = lons[-1]
      illat = np.where(lats>=llat)[0][0]
      iulat = np.where(lats>=ulat)[0][0]+1
      illon = np.where(lons>=llon)[0][0]
      iulon = np.where(lons>=ulon)[0][0]+1
   elif mode=='NAO':
      llat = 20
      ulat = 80
      llon = -90
      ulon = 40
      illat = np.where(lats>=llat)[0][0]
      iulat = np.where(lats>=ulat)[0][0]
      illon = np.where(lons>=llon)[0][0]
      iulon = np.where(lons>=ulon)[0][0]+1
   
   # change to match xarray!!!!
   varsub = var[:,illat:iulat,illon:iulon]
   latsub = lats[illat:iulat]
   lonsub = lons[illon:iulon]
   coslatsub = coslat[illat:iulat]

   return (varsub, latsub, lonsub, coslatsub)

#*********************************************************************************
# compute 2D (lat-lon) EOF with weighting and associated PC
def calc_EOF2D(anom, nplat, coslat, varcode):

   # apply sqrt cos latitude weighting
   wgts = np.sqrt(coslat)
   wgts = wgts[:,np.newaxis]

   # leading EOF
   solver =  Eof(anom, weights=wgts)
   eof1 = solver.eofs(neofs=1, eofscaling=0)[0]
   if varcode=='PSL':
      if eof1[np.where(nplat>=68)[0][0],0] > 0: # PSL 
         eof1 = -eof1
   elif varcode=='Z3':
      #if eof1[np.where(nplat>=80)[0][0],0] > 0: # Z3
      if eof1[np.where(nplat>=75)[0][0],0] > 0: # Z3
         eof1 = -eof1
   elif varcode=='U':
      if eof1[np.where(nplat>=60)[0][0],0] < 0: # U
         eof1 = -eof1
   
   # leading principal component
   PC1 = np.empty([anom.shape[0]])
   for itime in range(anom.shape[0]):
      PC1[itime] = np.dot(anom[itime,:,:].flatten(), eof1.flatten())

   return (eof1, PC1)

#*********************************************************************************
# projection of anomaly timeseries onto given EOF; standardized by Base PC
def projection(anom, eof, PCbase):
   
   # projection onto EOF
   PC = np.empty([anom.shape[0]])
   for itime in range(anom.shape[0]):
      PC[itime] = np.dot(anom[itime,...].flatten(), eof.flatten()) / PCbase.std()

   return PC

#*************************************************************************************
# plot EOF as regression map
def plot_EOF(anom, PC, lats, lons):

   outdir="/Users/abanerjee/scripts/glens/output/"

   # Plot the leading EOF expressed as regression map 
   PC = PC/PC.std()
   eofreg = np.empty([len(lats), len(lons)])
   for ilat in range(len(lats)):
      for ilon in range(len(lons)):
         eofreg[ilat,ilon] = ss.linregress(PC, anom[:,ilat,ilon])[0] / 100. # hPa per stdev
   
   fig = plt.figure()
   proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
   ax = plt.axes(projection=proj)
   ax.coastlines()
   ax.set_global()
   CS = ax.contourf(lons, lats, eofreg, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
   plt.colorbar(CS)
   ax.set_title('EOF1 regression map', fontsize=16)
   plt.savefig(outdir+'NAO_BaseEOF.png')
   plt.close()

#*************************************************************************************
# END #
#*************************************************************************************
