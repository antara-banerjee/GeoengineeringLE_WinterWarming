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
import EOF_defs2

# temporary
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#*********************************************************************************
# inputs
varcode='PSL'
season='DJF'
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
   npvar, nptime, nplat, nplon, coslat = EOF_defs2.preprocess(filename, varcode, 2010, 2030, vertical=False)
   npvars.append(npvar)

ntime = len(nptime)
nlat  = len(nplat)
nlon  = len(nplon)

npvars = np.array(npvars)
npvars = np.reshape(np.array(npvars), (nBase*ntime, nlat, nlon)); print(npvars.shape)

# monthly control climatology
clim = np.empty([12, nlat, nlon])
for i in range(12):
   clim[i,...] = npvars[i::12,...].mean(axis=0)   
print(clim[:,0,0])

# remove monthly climatology and seasonal mean
anom = EOF_defs2.calc_anom(npvars, clim, season)

# area subset
anomsub, nplatsub, nplonsub, coslatsub = EOF_defs2.area_subset(anom, 'NAO', nplat, nplon, coslat)
#anomsub = anom
print('variable',anomsub[0,0,0])
print('variable',anomsub.shape)
#nplatsub = nplat
#nplonsub = nplon
#coslatsub = coslat
   
# calculate EOF
eof1, PC1 = EOF_defs2.calc_EOF2D(anomsub, nplatsub, coslatsub)

# save leading EOF, PC and climatology to file
if save:
   np.save(npydir+'NAO-'+varcode+'_EOF_'+season, eof1)
   np.save(npydir+'NAO-'+varcode+'_PCbase_'+season, PC1)
   np.save(npydir+'NAO-'+varcode+'_clim_'+season, clim)

# plot EOF 
EOF_defs2.plot_EOF(anomsub, PC1, nplatsub, nplonsub)

#*************************************************************************************
# END #
#*************************************************************************************
