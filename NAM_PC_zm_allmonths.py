#*********************************************************************************
"""
Calculate NAM index as EOF of zonal mean geopotential height.
EOF is calculated from anomalies from global mean and from 
year round (deseasonalized) monthly mean data.
"""

#*********************************************************************************
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np
import xarray as xr
import glob
from cftime import DatetimeNoLeap
import scipy.stats as ss
from scipy import signal
import sys
from eofs.standard import Eof

# user modules
import ensemble_functions
import custom_colors as ccol
#from NAM_zm_allmonths import solver, coslatarray, eof1, wgts, eigenvalue1

#*********************************************************************************
# inputs
time_mean = 'DJF'
varcode="Z3"
eof1 = np.load('NAM_zm_EOF_nogm.npy')

#*************************************************************************************
# GLENS Feedback file
slopes = []
def projection(filename):
   
   # extract variable  
   var = xr.open_dataset(filename)[varcode] 

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset
   var = var.sel(time=slice(str(2020)+'-03-01', str(2095)+'-02-01'))

   # zonal mean
   var = var.mean(dim='lon', skipna=True)

   # latitude subset
   #var = var.sel(lat=slice(0,90))

   # convert variable and dimensions to numpy arrays - try later with xarray (xr.apply_ufunc)
   npvar = var.values
   nptime = var['time'].values
   global nplevel; nplevel = var['level'].values
   nplat = var['lat'].values

   # remove global mean
   global coslat; coslat = np.cos(np.deg2rad(nplat))
   global coslatarray; coslatarray = coslat[np.newaxis,np.newaxis,:]
   #npvar = npvar - npvar*coslatarray/np.sum(coslatarray)

   # latitude subset 
   npvar = npvar[:,:,np.where(nplat>=0)[0]]
   global nplathem; nplathem = nplat[nplat>0]
   coslatarray = coslatarray[:,:,nplat>0]
   coslat = coslat[nplat>0]

   # group by month and deseasonalize
   var_monthly = np.empty([int(len(nptime)/12), len(nplevel), len(nplathem), 12])
   for i in range(12):
      var_monthly[...,i] = npvar[i::12,...] - npvar[i::12,...].mean(axis=0)
   
   # deseasonalize
   #npvarDS = np.empty_like(npvar)
   #for i in range(len(nptime)):
   #   j = i%12
   #   npvarDS[i,...] = npvar[i,...] - npvar[j::12,...].mean(axis=0)

   print(npvarDS.shape)

   PCfeedback = np.empty([int(len(nptime)/12), len(nplevel), 12])
   for ilevel in range(len(nplevel)):
      for imonth in range(12):
         PC = np.dot(var_monthly[:,ilevel,:,imonth], eof1[ilevel,...]) 
   #      PCfeedback[:,ilevel,imonth] = PC
         PCfeedback[:,ilevel,imonth] = (PC-PC.mean())/PC.std()

   slope = np.empty([len(nplevel), 12])
   for ilevel in range(len(nplevel)):
      for imonth in range(12):
         slope[ilevel,imonth] = (ss.linregress(range(int(len(nptime)/12)), PCfeedback[:,ilevel,imonth])[0]) * 30  

   return slope

for i in range(1,2):
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+variable+".202001-*.nc")[0] 
   slope = projection(filename)
   slopes.append(slope)

# for single ensemble member to test
#PC_mean, PC_std = ensemble_functions.stats(PCs)
#slope_mean = slopes[0]
slope_mean = np.mean(np.array(slopes), axis=0)
# roll so that July is first (currently begins in March)
print(slope_mean[0,4])
slope_mean = np.roll(slope_mean,-4,axis=1)
print(slope_mean[0,0])

yticklabels = [1000,700,500,300,100,70,50,30,10,7,5,3,1]
cols = ccol.custom_colors('matlab')
fig = plt.figure()
shading = plt.contourf(range(12),-np.log10(nplevel),slope_mean,cmap=cols, extend='both')#, levels=np.arange(-1.8,2,0.2))
plt.yticks(-np.log10(yticklabels), yticklabels)
plt.xticks(range(12),['J','A','S','O','N','D','J','F','M','A','M','J'])
plt.colorbar(shading)
plt.ylim([-np.log10(1000), -np.log10(1)])
plt.xlabel('Month')
plt.ylabel('Pressure')
#plt.show()
plt.savefig('NAM_feedback.png')
plt.close()
#plt.savefig('NAO_'+time_mean+'_EOFBase.png')

