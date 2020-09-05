#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#*************************************************************************************
# NAO(SLP) EOF #
#*********************************************************************************
"""
Calculate NAO index as EOF of sea level pressure.

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
varcode="PSL"
save=False

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*********************************************************************************
def calc_EOF(filename):

   # extract variable  
   var = xr.open_dataset(filename)[varcode] 

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset - start in March, end in February
   var = var.sel(time=slice(str(2010)+'-03-01', str(2030)+'-02-01'))

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
   var = var.sel(lat=slice(20,80), lon=slice(-90,40))

   # convert variable and dimensions to numpy arrays 
   npvar = var.values
   global nptime; nptime = var['time'].values
   global nplat; nplat = var['lat'].values
   global nplon; nplon = var['lon'].values

   # for cos latitude weighting later
   global coslat; coslat = np.cos(np.deg2rad(nplat))

   return npvar

#*********************************************************************************
# Concatenate Base data 
npvars = []
nBase = 5 
for i in range(1,nBase+1):
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0] 
   print('Base run ',i)
   npvar = calc_EOF(filename)
   npvars.append(npvar)

npvars = np.array(npvars)
npvars = np.reshape(np.array(npvars), (nBase*len(nptime), len(nplat), len(nplon))); print(npvars.shape)

# monthly control climatology
clim = np.empty([12, len(nplat), len(nplon)])
for i in range(12):
   j = range(i, nBase*len(nptime), 12)
   clim[i,...] = npvars[j,...].mean(axis=0)   

# remove monthly climatology
npvarDS = np.empty_like(npvars)
for i in range(nBase*len(nptime)):
   j = i%12
   npvarDS[i,...] = npvars[i,...] - clim[j] 

nyrs = int(npvarDS.shape[0]/12)
npvarSEAS = np.empty([nyrs, npvarDS.shape[1], npvarDS.shape[2]])
for i in range(nyrs):
   j = 9+(12*i)
   npvarSEAS[i,...] = npvarDS[j:j+3,...].mean(axis=0)
   
# compute EOFs at each level
wgts = np.sqrt(coslat)
wgts = wgts[:,np.newaxis]

#solver =  Eof(npvarDS, weights=wgts)
solver =  Eof(npvarSEAS, weights=wgts)
eof1 = solver.eofs(neofs=1, eofscaling=0)[0]
if eof1[np.where(nplat>=68)[0][0],0] > 0:
   eof1 = -eof1

'''
# same as above; need to figure out handling of missing values
wgtsanom = anoms*wgts; print(anoms.shape)
#eof1 = np.empty([len(nplevel), len(nplat)])
eof1 = np.empty([29, len(nplat)])
for ilevel in range(29):
    cov = np.cov(np.transpose(wgtsanom[:,ilevel,:]))
    evals, evecs = LA.eig(cov)
    eof1[ilevel,:] = evecs[:,0]
    #print('here', eof1.shape)
'''

# Base leading principal component
PCbase = np.empty([npvarDS.shape[0]])
for itime in range(npvarDS.shape[0]):
   PCbase[itime] = np.dot(npvarDS[itime,:,:].flatten(), eof1.flatten())

# save leading EOF, PC and climatology to file
if save:
   np.save(npydir+'NAO-SLP_EOF_allmonths', eof1)
   np.save(npydir+'NAO-SLP_PCbase_allmonths', PCbase)
   np.save(npydir+'NAO-SLP_clim_allmonths', clim)

#*************************************************************************************
# Plot the leading EOF expressed as regression map 

# regression of EOF against standardized PC
PCbase = PCbase/PCbase.std()
eof1reg = np.empty([len(nplat), len(nplon)])
for ilat in range(len(nplat)):
   for ilon in range(len(nplon)):
      eof1reg[ilat,ilon] = ss.linregress(PCbase, npvarDS[:,ilat,ilon])[0] / 100. # hPa per stdev

fig = plt.figure()
proj = ccrs.Orthographic(central_longitude=-20, central_latitude=60)
ax = plt.axes(projection=proj)
ax.coastlines()
ax.set_global()
CS = ax.contourf(nplon, nplat, eof1reg, cmap=plt.cm.RdBu_r, transform=ccrs.PlateCarree())
plt.colorbar(CS)
ax.set_title('EOF1 regression map', fontsize=16)
plt.savefig(outdir+'NAO_BaseEOF.png')
plt.close()
#*************************************************************************************
# END #
#*************************************************************************************
