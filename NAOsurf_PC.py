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
#from control_NAO_EOF import eof1, PCbase, clim

#*********************************************************************************
# inputs
time_mean = 'JJA'
varcode="PSL"
save=True

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

startmonth = {'DJF':9,'MAM':0,'JJA':3,'SON':6}
istartmonth = startmonth[time_mean]

#*************************************************************************************
# load EOF, PC and control climatology
eof1 = np.load(npydir+'NAO-'+varcode+'_EOF.npy')
PCbase = np.load(npydir+'NAO-'+varcode+'_PCbase.npy')
clim = np.load(npydir+'NAO-'+varcode+'_clim.npy')

#*************************************************************************************
slopes = []
def projection(filename):
   
   # extract variable  
   var = xr.open_dataset(filename)[varcode] 

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset - start in March, end in February
   var = var.sel(time=slice(str(2020)+'-03-01', str(2095)+'-02-01')) #***GEOHEAT

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

   # remove control climatology 
   npvarDS = np.empty_like(npvar)
   for i in range(len(nptime)):
      j = i%12 
      npvarDS[i,...] = npvar[i,...] - clim[j,...]

   # seasonal mean
   npvarSEAS = np.empty([int(len(nptime)/12),len(nplat),len(nplon)])
   for i in range(int(len(nptime)/12)): 
      j = 12*i+istartmonth
      npvarSEAS[i,...] = npvarDS[j:j+3,...].mean(axis=0)

   # projection onto EOF
   PCfeedbackSEAS = np.empty([int(len(nptime)/12)])
   for itime in range(int(len(nptime)/12)):
      PCfeedbackSEAS[itime] = np.dot(npvarSEAS[itime,...].flatten(), eof1.flatten()) / PCbase.std()

   # projection onto EOF
   #PCfeedback = np.empty([len(nptime)])
   #for itime in range(len(nptime)):
   #   #PCfeedback[itime] = (np.dot(npvarDS[itime,...].flatten(), eof1.flatten()) - PCbase.mean()) / PCbase.std()
   #   PCfeedback[itime] = (np.dot(npvarDS[itime,...].flatten(), eof1.flatten())) / PCbase.std()

   # seasonal mean
   #PCfeedbackSEAS = np.empty([int(len(nptime)/12)])
   #for i in range(int(len(nptime)/12)): 
   #   j = 12*i+istartmonth
   #   #PCfeedbackSEAS[i] = PCfeedbackSTD[j:j+3].mean()
   #   PCfeedbackSEAS[i] = PCfeedback[j:j+3].mean()

   return PCfeedbackSEAS

PCfeedbacks = []
for i in range(1,21):
   print('Feedback run ',i)
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0] 
   PCfeedback = projection(filename)
   #np.save(npydir+'NAO-SLP_'+time_mean+'_PC_feedback_'+str(i)+'.npy', PCfeedback) 
   np.save(npydir+'NAO-'+varcode+'_'+time_mean+'_PC_feedback_'+str(i)+'_JJA.npy', PCfeedback) 
   #PCfeedback = np.load(npydir+'NAO-SLP_'+time_mean+'_PC_feedback_'+str(i)+'.npy') 
   PCfeedbacks.append(PCfeedback)

'''
PCrcp85s = []
for i in range(1,4):
   print('Base run ',i)
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0] 
   PCrcp85 = projection(filename)
   np.save(npydir+'NAO-SLP_'+time_mean+'_PC_RCP85_'+str(i)+'.npy', PCrcp85) 
   PCrcp85s.append(PCrcp85)
'''
'''
PCgeoheats = []
for i in range(1,5):
   for yr in range(2011,2031):
      filename = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+varcode+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
      PCgeoheat = projection(filename)
      PCgeoheats.append(PCgeoheat)

PCgeoheats = np.array(PCgeoheats).flatten()
run1 = PCgeoheats[:20].mean()
run2 = PCgeoheats[20:40].mean()
run3 = PCgeoheats[40:60].mean()
run4 = PCgeoheats[60:80].mean()
print(run1, run2, run3, run4)
print(PCgeoheats.mean(), PCgeoheats.std())

fig = plt.figure()
plt.hist(PCgeoheats, bins=10, density=True)
plt.axvline(x=0)
plt.axvline(x=PCgeoheats.mean(), color='k')
plt.savefig('hist.png')
plt.close()
'''

