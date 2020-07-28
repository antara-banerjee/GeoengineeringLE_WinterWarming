#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#*************************************************************************************
# NAM CALCULATION #
#*********************************************************************************
"""
Calculate NAO index as EOF of sea level pressure.
EOF is calculated from anomalies from global mean and from 
year round (deseasonalized) monthly mean data.

@author: A Banerjee
"""

#*********************************************************************************
import numpy as np
import xarray as xr
import glob
from cftime import DatetimeNoLeap
from eofs.standard import Eof
from numpy import linalg as LA
import scipy.stats as ss

# temporary
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#*********************************************************************************
# inputs
variable="PSL"
outdir="/Users/abanerjee/scripts/glens/output/"

#*********************************************************************************
# MAIN

def calc_EOF(filename):

   # extract variable  
   var = xr.open_dataset(filename)[variable] / 100 # sea level pressure in hPa

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset - start in March, end in February
   var = var.sel(time=slice(str(2010)+'-03-01', str(2030)+'-02-01'))

   # Adjust lon values to make sure they are within (-180, 180)
   lon_name = 'lon'  # whatever name is in the data

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
   var = var.sel(lat=slice(20,80), lon=slice(-90,40))

   # convert variable and dimensions to numpy arrays - try later with xarray (xr.apply_ufunc)
   npvar = var.values
   global nptime; nptime = var['time'].values
   global nplat; nplat = var['lat'].values
   global nplon; nplon = var['lon'].values

   # remove global mean
   global coslat; coslat = np.cos(np.deg2rad(nplat))
   global coslatarray; coslatarray = coslat[np.newaxis,:,np.newaxis]
   #npvar = npvar - npvar*coslatarray/np.sum(coslatarray)

   # deseasonalize
   npvarDS = np.empty_like(npvar)
   for i in range(len(nptime)):
      j = i%12
      npvarDS[i,...] = npvar[i,...] - npvar[j::12,...].mean(axis=0)

   # detrend
   #for ilat in range(len(nplat)):
   #   for ilon in range(len(nplon)):
   #      x = np.arange(int(len(nptime)))
   #      y = npvarDS[:,ilat,ilon]
   #      m, b, r_val, p_val, std_err = ss.linregress(x,y)
   #      npvarDS[:,ilat,ilon] = npvarDS[:,ilat,ilon] - (m*x + b)
      
   ## detrend by month
   #for ilat in range(len(nplat)):
   #   for ilon in range(len(nplon)):
   #      for imonth in range(12):
   #         x = np.arange(int(len(nptime)/12))
   #         y = npvarDS[imonth::12,ilat,ilon]
   #         m, b, r_val, p_val, std_err = ss.linregress(x,y)
   #         npvarDS[imonth::12,ilat,ilon] = npvarDS[imonth::12,ilat,ilon] - (m*x + b)

   return npvarDS

anoms = []
nBase = 20
for i in range(1,nBase+1):
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+variable+".201001-*.nc")[0] 
   print('Base run ',i)
   anom = calc_EOF(filename)
   anoms.append(anom)

anoms = np.array(anoms); print(anoms.shape)
anoms = np.reshape(np.array(anoms), (nBase*len(nptime), len(nplat), len(nplon))); print(anoms.shape)
   
# compute EOFs at each level
wgts = np.sqrt(coslat)
wgts = wgts[:,np.newaxis]

'''
# same as below; need to figure out handling of missing values
wgtsanom = anoms*wgts; print(anoms.shape)
#eof1 = np.empty([len(nplevel), len(nplat)])
eof1 = np.empty([29, len(nplat)])
for ilevel in range(29):
    cov = np.cov(np.transpose(wgtsanom[:,ilevel,:]))
    evals, evecs = LA.eig(cov)
    eof1[ilevel,:] = evecs[:,0]
    #print('here', eof1.shape)

print(eof1)
'''

solver =  Eof(anoms, weights=wgts)
eof1 = solver.eofs(neofs=1, eofscaling=0)[0]
if eof1[np.where(nplat>=70)[0][0],0] > 0:
   eof1 = -eof1
   #eigenvalue1[ilevel] = solver.eigenvalues(neigs=1)
   # check eigenvector is unit length
   #x = np.sum(eof1[ilevel,:]**2)
   #print(x)

     
#*************************************************************************************
# Plot the leading EOF expressed as covariance in the European/Atlantic domain.
#clevs = np.linspace(-75, 75, 11)
fig = plt.figure()
proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
ax = plt.axes(projection=proj)
ax.coastlines()
ax.set_global()
##eof1[0].plot.contourf(ax=ax, levels=clevs, cmap=plt.cm.RdBu_r,
CS = ax.contourf(nplon, nplat, eof1, cmap=plt.cm.RdBu_r,
                         transform=ccrs.PlateCarree())
plt.colorbar(CS)
#ax.set_title('EOF1 expressed as covariance', fontsize=16)
plt.savefig(outdir+'NAO_BaseEOF.png')
plt.close()
#*************************************************************************************
# END #
#*************************************************************************************
