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
import EOF_defs2

# temporary
import matplotlib.pyplot as plt

#*********************************************************************************
# inputs
varcode='U'
season = 'DJF'
save=False
mode='NAO'

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*************************************************************************************
# 1) Concatenate Base data 
npvars = []
nBase = 20 
for run in range(1,nBase+1):

   print('Base run ',run)
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(run).zfill(2)+"/atm/proc/tseries/month_1/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(run).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0] 

   npvar, nptime, nplev, nplat, nplon, coslat = EOF_defs2.preprocess(filename, varcode, 2010, 2030, vertical=True)
   npvars.append(npvar)

ntime = len(nptime)
nlat  = len(nplat)
nlon  = len(nplon)
nlev  = len(nplev)  # additional to surface script

npvars = np.array(npvars); print(npvars.shape)
npvars = np.reshape(np.array(npvars), (nBase*ntime, nlev, nlat, nlon)); print(npvars.shape)

#np.save(npydir+mode+'-'+varcode+'_concatBase.npy', npvars)

##*********************************************************************************
## 2) Remove global mean if using geopotential height
#print('remove global mean')
#coslat = np.cos(np.deg2rad(nplat))
#coslatarray = coslat[np.newaxis,np.newaxis,:,np.newaxis]
#if varcode=='Z3':
#   gm = np.nansum(control*coslatarray, axis=2)/np.sum(coslatarray)
#   print(gm.shape, control.shape)
#   control = control - gm[:,:,np.newaxis,:]

#*********************************************************************************
eofBase = np.empty([nlev,nlat,nlon]) 
PCBase = np.empty([int(nBase*ntime/12),nlev]) 
climBase = np.empty([12,nlev,nlat,nlon]) 

for ilev in range(nlev):

   print('level: ', ilev, nplev[ilev])
   x = npvars[:,ilev,:,:]

   # monthly control climatology
   clim = np.empty([12, nlat, nlon])
   for i in range(12):
      clim[i,...] = x[i::12,...].mean(axis=0)
   
   # remove monthly climatology and seasonal mean
   anom = EOF_defs2.calc_anom(x, clim, season)

   # area subset
   anomsub, latsub, lonsub, coslatsub = EOF_defs2.area_subset(anom, 'NAO', nplat, nplon, coslat)

   # calculate EOF
   eof1, PC1 = EOF_defs2.calc_EOF2D(anomsub, latsub, coslatsub)

   # change dimensions
   eofBase = eofBase[:,:len(latsub),:len(lonsub)] 

   eofBase[ilev,:,:] = eof1
   PCBase[:,ilev] = PC1 
   climBase[:,ilev,:,:] = clim 
   #eofBase[ilev] = eof1
   #PCBase[ilev] = PC1 
   #climBase[ilev] = clim 

print(eofBase.shape, PCBase.shape, climBase.shape)
# save leading EOF, PC and climatology to file
if save:
   np.save(npydir+mode+'-'+varcode+'_vertical_EOF_'+season, eofBase)
   np.save(npydir+mode+'-'+varcode+'_vertical_PCbase_'+season, PCBase)
   np.save(npydir+mode+'-'+varcode+'_vertical_clim_'+season, climBase)

quit()

#*************************************************************************************
fig = plt.figure()
plt.plot(nplatsub, controlEOF[np.where(nplevel==50)[0][0],...].mean(axis=1)*coslat, label='50hPa')
plt.plot(nplatsub, controlEOF[np.where(nplevel==500)[0][0],...].mean(axis=1)*coslat, label='500hPa')
plt.plot(nplatsub, controlEOF[np.where(nplevel==850)[0][0],...].mean(axis=1)*coslat, label='850hPa')
plt.plot(nplatsub, controlEOF[np.where(nplevel==950)[0][0],...].mean(axis=1)*coslat, label='950hPa')
plt.title('EOF1 regression pattern', fontsize=16)
plt.xlim([0,90])
plt.legend()
plt.savefig(outdir+mode+'-'+varcode+'_EOF.png')
plt.close()

#*************************************************************************************
# END #
#*************************************************************************************
