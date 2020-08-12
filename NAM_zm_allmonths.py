#*************************************************************************************
# NAM CALCULATION #
#*********************************************************************************
"""
Calculate NAM index as EOF of zonal mean geopotential height.
EOF is calculated from anomalies from global mean and from 
year round (deseasonalized) monthly mean data.
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

#*********************************************************************************
# inputs
varcode="Z3"

#*********************************************************************************
# MAIN
def calc_anom(filename):

   # extract variable  
   var = xr.open_dataset(filename)[varcode] 

   # modify time coordinate for CESM (1 month backwards)
   oldtime = var['time']
   newtime_beg = DatetimeNoLeap(oldtime.dt.year[0],oldtime.dt.month[0]-1,oldtime.dt.day[0])
   newtime = xr.cftime_range(start=newtime_beg, periods=np.shape(oldtime)[0], freq='MS', calendar='noleap')
   var = var.assign_coords(time=newtime)

   # time subset
   var = var.sel(time=slice(str(2010)+'-03-01', str(2030)+'-02-01'))

   # zonal mean
   var = var.mean(dim='lon', skipna=True)

   # latitude subset
   #var = var.sel(lat=slice(0,90))

   # convert variable and dimensions to numpy arrays - try later with xarray (xr.apply_ufunc)
   npvar = var.values
   global nptime; nptime = var['time'].values
   global nplevel; nplevel = var['level'].values
   global nplat; nplat = var['lat'].values

   # remove global mean
   global coslat; coslat = np.cos(np.deg2rad(nplat))
   global coslatarray; coslatarray = coslat[np.newaxis,np.newaxis,:]
   # removing global mean causes problems with nan
   #gm = np.sum(npvar*coslatarray, axis=2)/np.sum(coslatarray); print('gm shape: ',gm.shape)
   #npvar = npvar - gm[:,:,np.newaxis]

   # latitude subset 
   npvar = npvar[:,:,np.where(nplat>=0)[0]]
   global nplathem; nplathem = nplat[nplat>0]
   coslatarray = coslatarray[:,:,nplat>0]
   coslat = coslat[nplat>0]

   # deseasonalize
   npvarDS = np.empty_like(npvar)
   for i in range(len(nptime)):
      j = i%12
      npvarDS[i,...] = npvar[i,...] - npvar[j::12,...].mean(axis=0)
      
   return npvarDS

#*************************************************************************************
# Anomalies for input into EOF calculation
anoms = []
nBase = 20
for i in range(1,nBase+1):
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+variable+".201001-*.nc")[0] 
   print('Base run ',i)
   anom = calc_anom(filename)
   anoms.append(anom)

anoms = np.array(anoms); print(anoms.shape)
anoms = np.reshape(np.array(anoms), (nBase*len(nptime), len(nplevel), len(nplathem))); print(anoms.shape)
   
#*************************************************************************************
# compute EOFs at each level
wgts = np.sqrt(coslat)

eof1 = np.empty([len(nplevel), len(nplathem)])
eigenvalue1 = np.empty([len(nplevel)])
for ilevel in range(len(nplevel)):

   # EOF
   solver =  Eof(anoms[:,ilevel,:], weights=wgts)
   eof1[ilevel,:] = solver.eofs(neofs=1, eofscaling=0)[0]
   if eof1[ilevel,np.where(nplathem>=70)[0][0]] > 0:
       eof1[ilevel,:] = -eof1[ilevel,:]

   # standardized PC
   #PC1 = np.dot(anoms[:,ilevel,:], eof1[ilevel,:])
   #PC1 = (PC1-PC1.mean())/PC1.std()

   # regression
   #for ilat in range(len(nplathem)):
   #   eof1[ilevel,ilat] = ss.linregress(PC1, anoms[:,ilevel,ilat])[0]

#np.save('NAM_zm_EOF_nogm_unitless', eof1)

'''
# same as above; need to figure out handling of missing values
wgtsanom = anoms*wgts; print(anoms.shape)
#eof1 = np.empty([len(nplevel), len(nplat)])
eof1 = np.empty([29, len(nplat)])
for ilevel in range(29):
    cov = np.cov(np.transpose(wgtsanom[:,ilevel,:]))
    evals, evecs = LA.eig(cov)
    eof1[ilevel,:] = evecs[:,0]
'''

#*************************************************************************************
fig = plt.figure()
plt.plot(nplathem, eof1[np.where(nplevel[:29]==50)[0][0],:]*coslat, color='r', label='50hPa')
plt.plot(nplathem, eof1[np.where(nplevel[:29]==10)[0][0],:]*coslat, color='g', label='10hPa')
plt.plot(nplathem, eof1[np.where(nplevel[:29]==1)[0][0],:]*coslat, color='b', label='1hPa')
#plt.plot(nplat, eof1[np.where(nplevel==950)[0][0],:]*coslat, color='k', label='950hPa')
#plt.plot(nplat, eof1[np.where(nplevel==750)[0][0],:]*coslat, color='r', label='750hPa')
#plt.plot(nplat, eof1[np.where(nplevel==550)[0][0],:]*coslat, color='g', label='550hPa')
#plt.plot(nplat, eof1[np.where(nplevel==350)[0][0],:]*coslat, color='b', label='350hPa')
plt.title('EOF1 regression pattern', fontsize=16)
plt.xlim([0,90])
plt.legend()
plt.savefig('NAM_EOF.png')
plt.close()

#*************************************************************************************
# END #
#*************************************************************************************
