'''
Compute leading EOF of concatenated Base run surface fields. 

-Mode can be NAM or NAO index based on e.g. sea level pressure fields.  
'''

# standard imports
import glob
import numpy as np

# user imports
import PCA_defs 

#*********************************************************************************
# inputs
varcode='PSL'
season='JJA'
mode='NAO'
save=True

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*********************************************************************************
# concatenate Base data 
npvars = []
nBase = 20 
for i in range(1,nBase+1):
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0] 
   print('Base run ',i)
   npvar, nptime, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, 2010, 2030, vertical=False)
   npvars.append(npvar)

ntime = len(nptime)
nlat  = len(nplat)
nlon  = len(nplon)

npvars = np.array(npvars)
npvars = np.reshape(np.array(npvars), (nBase*ntime, nlat, nlon))
print('Concatenated Base shape: ',npvars.shape)

# monthly Base climatology
clim = np.empty([12, nlat, nlon])
for i in range(12):
   clim[i,...] = npvars[i::12,...].mean(axis=0)   

# remove monthly climatology and seasonal mean
# similar results obtained from using year-round Base anomalies
anom = PCA_defs.calc_anom(npvars, clim, season)

# area subset
anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, mode, nplat, nplon, coslat)
   
# calculate EOF
eof1, PC1 = PCA_defs.calc_EOF2D(anomsub, nplatsub, coslatsub, varcode)

# save leading EOF, PC and climatology to file
if save:
   np.save(npydir+mode+'-'+varcode+'_EOF_'+season, eof1)
   np.save(npydir+mode+'-'+varcode+'_PCbase_'+season, PC1)
   np.save(npydir+mode+'-'+varcode+'_clim_'+season, clim)

# plot EOF 
PCA_defs.plot_EOF(anomsub, PC1, nplatsub, nplonsub)

#*************************************************************************************
# END #
#*************************************************************************************
