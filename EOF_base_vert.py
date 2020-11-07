'''
Compute leading EOF of concatenated Base vertical fields.

-Mode can be NAM or NAO based on e.g. geopotential height or zonal wind fields.
'''

# standard imports
import glob
import matplotlib.pyplot as plt
import numpy as np

# user imports
import PCA_defs 

#*********************************************************************************
# inputs
varcode='Z3'
season = 'DJF'
save=True
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

   npvar, nptime, nplev, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, 2010, 2030, vertical=True)
   npvars.append(npvar)

ntime = len(nptime)
nlat  = len(nplat)
nlon  = len(nplon)
nlev  = len(nplev)  # additional to surface script

npvars = np.array(npvars)
npvars = np.reshape(np.array(npvars), (nBase*ntime, nlev, nlat, nlon))
print('Concatenated Base shape: ',npvars.shape)

#*********************************************************************************
eofBase = np.empty([nlev,nlat,nlon]) 
PCBase = np.empty([int(nBase*ntime/12),nlev]) 
climBase = np.empty([12,nlev,nlat,nlon]) 

for ilev in range(nlev):

   print('level: ', ilev, nplev[ilev])
   x = npvars[:,ilev,:,:]

   # remove global mean if using geopotential height
   if varcode=='Z3':
      x = PCA_defs.remove_gm(x, nplat, coslat)

   # monthly control climatology
   clim = np.empty([12, nlat, nlon])
   for i in range(12):
      clim[i,...] = x[i::12,...].mean(axis=0)
   
   # remove monthly climatology and seasonal mean
   anom = PCA_defs.calc_anom(x, clim, season)

   # area subset
   anomsub, latsub, lonsub, coslatsub = PCA_defs.area_subset(anom, mode, nplat, nplon, coslat)

   # calculate EOF
   eof1, PC1 = PCA_defs.calc_EOF2D(anomsub, latsub, coslatsub, varcode=varcode)

   # change dimensions
   eofBase = eofBase[:,:len(latsub),:len(lonsub)] 

   eofBase[ilev,:,:] = eof1
   PCBase[:,ilev] = PC1 
   climBase[:,ilev,:,:] = clim 

# save leading EOF, PC and climatology to file
if save:
   np.save(npydir+mode+'-'+varcode+'_vertical_EOF_'+season, eofBase)
   np.save(npydir+mode+'-'+varcode+'_vertical_PCbase_'+season, PCBase)
   np.save(npydir+mode+'-'+varcode+'_vertical_clim_'+season, climBase)

#*************************************************************************************
# Visualize zonal means EOFs at different heights 
fig = plt.figure()
plt.plot(latsub, eofBase[np.where(nplev==50)[0][0],...].mean(axis=1)*coslatsub, label='50hPa')
plt.plot(latsub, eofBase[np.where(nplev==500)[0][0],...].mean(axis=1)*coslatsub, label='500hPa')
plt.plot(latsub, eofBase[np.where(nplev==850)[0][0],...].mean(axis=1)*coslatsub, label='850hPa')
plt.plot(latsub, eofBase[np.where(nplev==950)[0][0],...].mean(axis=1)*coslatsub, label='950hPa')
plt.title('EOF1', fontsize=16)
plt.xlim([0,90])
plt.legend()
plt.savefig(outdir+mode+'-'+varcode+'_EOF.png')
plt.close()

#*************************************************************************************
# END #
#*************************************************************************************
