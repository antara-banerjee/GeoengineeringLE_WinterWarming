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
from nao_index_amy import ensmean

#*********************************************************************************
# inputs
variable="PSL"
time_mean = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"

#*********************************************************************************
# MAIN

def calc_anomaly(filename):

   # extract variable  
   var = xr.open_dataset(filename)[variable] / 100 # sea level pressure in hPa

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset - start in March, end in February
   var = var.sel(time=slice(str(2020)+'-03-01', str(2095)+'-02-01'))

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
   var = var.sel(lat=slice(20,70), lon=slice(-90,40))

   # monthly anomalies
   varDS = var.groupby('time.month') - var.groupby('time.month').mean('time')

   # annual seasonal mean
   ASseas= {'DJF':'DEC',
            'MAM':'MAR',
            'JJA':'JUN',
            'SON':'SEP'}
   varSEAS = varDS.sel(time=(varDS['time.season']==time_mean)) # select based on boolean array
   varYRMN = varSEAS.resample(time='AS-'+ASseas[time_mean]).mean()

   # detrend
   varDT = varYRMN - varYRMN.mean('time')

   # convert variable and dimensions to numpy arrays - try later with xarray (xr.apply_ufunc)
   tseries = varYRMN.values 
   tseriesANOM = varDT.values
   global nptime; nptime = varDT['time'].values
   global nplat; nplat = varDT['lat'].values

   # remove global mean
   global coslat; coslat = np.cos(np.deg2rad(nplat))
   global coslatarray; coslatarray = coslat[np.newaxis,:,np.newaxis]
   #npvar = npvar - npvar*coslatarray/np.sum(coslatarray)

   return (tseries, tseriesANOM) 

def calc_EOF(anomaly_field):
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
   
   solver =  Eof(anomaly_field, weights=wgts)
   eof1 = solver.eofs(neofs=1, eofscaling=0)[0]
   if eof1[np.where(nplat>=68)[0][0],0] > 0:
      eof1 = -eof1
      #eigenvalue1[ilevel] = solver.eigenvalues(neigs=1)
      # check eigenvector is unit length
      #x = np.sum(eof1[ilevel,:]**2)
      #print(x)

   return eof1

def calc_PC(timeseries, eof):

   PC = np.empty([len(nptime)])
   for itime in range(len(nptime)):
      PC[itime] = np.dot(timeseries[itime,...].flatten(), eof.flatten())

   # standardize seasonal mean PC by 2020-2040 climatology
   PCstandard= (PC - PC[:21].mean())/PC[:21].std() 

   return PCstandard

PCfeedbacks = []
nrun = 20 
for i in range(1,nrun+1):

   print('Feedback run ',i)
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+variable+".202001-*.nc")[0] 

   tseries, tseries_anom = calc_anomaly(filename)
   eof1 = calc_EOF(tseries_anom)
   PC1 = calc_PC(tseries, eof1)

   PCfeedbacks.append(PC1)

#*************************************************************************************
# for single ensemble member to test
#PC_mean, PC_std = ensemble_functions.stats(PCs)
#slope_mean = slopes[0]
PC_mean = np.mean(np.array(PCfeedbacks), axis=0)
print(PC_mean.shape)

fig = plt.figure(figsize=(8,4))
plt.plot(np.arange(2020,2095), PC_mean, color='k')
plt.fill_between(x=np.arange(2020,2095), y1=0, y2=PC_mean, where=PC_mean>0, color='r', interpolate=True)
plt.fill_between(x=np.arange(2020,2095), y1=0, y2=PC_mean, where=PC_mean<0, color='b', interpolate=True)
plt.plot(np.arange(2020,2096), ensmean, linestyle='-', color='green', linewidth=1.5)
plt.xlabel('Year')
plt.ylabel('NAO index')
plt.xlim([2020,2100])
plt.ylim([-0.7,0.7])
plt.savefig(outdir+'NAO_PCfeedback.png')
plt.close()
#*************************************************************************************
# END #
#*************************************************************************************
