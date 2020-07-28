#*********************************************************************************
"""
NAO index
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
from NAO_EOF_allmonths import eof1

#*********************************************************************************
# inputs
time_mean = 'DJF'
variable="PSL"
outdir="/Users/abanerjee/scripts/glens/output/"

startmonth = {'DJF':9,'MAM':0,'JJA':3,'SON':6}
istartmonth = startmonth[time_mean]

#*************************************************************************************
# GLENS Feedback file
slopes = []
def projection(filename):
   
   # extract variable  
   var = xr.open_dataset(filename)[variable] 

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset - start in March, end in February
   var = var.sel(time=slice(str(2020)+'-03-01', str(2095)+'-02-01'))

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

   # convert variable and dimensions to numpy arrays - try later with xarray (xr.apply_ufunc)
   npvar = var.values
   global nptime; nptime = var['time'].values
   global nplat; nplat = var['lat'].values
   global nplon; nplon = var['lon'].values

   # remove global mean
   #global coslat; coslat = np.cos(np.deg2rad(nplat))
   #global coslatarray; coslatarray = coslat[np.newaxis,:,np.newaxis]
   #npvar = npvar - npvar*coslatarray/np.sum(coslatarray)

   # deseasonalize
   npvarDS = np.empty_like(npvar)
   for i in range(len(nptime)):
      j = i%12 
      npvarDS[i,...] = (npvar[i,...] - npvar[j::12,...].mean(axis=0)) 

   #npvarDS = npvarDS - npvarDS[:12*21,...].mean(axis=0) # or calculate anomalies first

   # projection onto EOF
   PCfeedback = np.empty([len(nptime)])
   for itime in range(len(nptime)):
      PCfeedback[itime] = np.dot(npvarDS[itime,...].flatten(), eof1.flatten()) 
         
   # standardize each month by its 2020-2040 climatology   
   PCfeedbackSTD = np.empty_like(PCfeedback)
   for itime in range(len(nptime)):
      j = itime%12
      PCfeedbackSTD[itime] = (PCfeedback[itime] - PCfeedback[j:12*21:12].mean()) / PCfeedback[j:12*21:12].std() 

   # standardize by year round 2020-2040 climatology 
   #PCfeedbackSTD = (PCfeedback - PCfeedback[0:12*21].mean()) / PCfeedback[0:12*21].std() 

   PCfeedbackSEAS = np.empty([int(len(nptime)/12)])
   for i in range(int(len(nptime)/12)): 
      j = 12*i+istartmonth
      PCfeedbackSEAS[i] = PCfeedbackSTD[j:j+3].mean()
      #PCfeedbackSEAS[i] = PCfeedback[j:j+3].mean()

   # standardize seasonal mean PC by 2020-2040 climatology
   #PCfeedbackSEAS = (PCfeedbackSEAS - PCfeedbackSEAS[:21].mean())/PCfeedbackSEAS[:21].std() 

   return PCfeedbackSEAS

PCfeedbacks = []
for i in range(1,21):
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+variable+".202001-*.nc")[0] 
   PCfeedback = projection(filename)
   print('Feedback run ',i)
   PCfeedbacks.append(PCfeedback)

# for single ensemble member to test
#PC_mean, PC_std = ensemble_functions.stats(PCs)
#slope_mean = slopes[0]
PC_mean = np.mean(np.array(PCfeedbacks), axis=0)
print(PC_mean.shape)

fig = plt.figure(figsize=(8,4))
plt.plot(np.arange(2020,2095), PC_mean, color='k')
plt.fill_between(x=np.arange(2020,2095), y1=0, y2=PC_mean, where=PC_mean>0, color='r', interpolate=True)
plt.fill_between(x=np.arange(2020,2095), y1=0, y2=PC_mean, where=PC_mean<0, color='b', interpolate=True)
plt.xlabel('Year')
plt.ylabel('NAO index')
plt.xlim([2020,2100])
plt.ylim([-0.6,0.6])
plt.savefig(outdir+'NAO_PCfeedback.png')
plt.close()
#plt.savefig('NAO_'+time_mean+'_EOFBase.png')

