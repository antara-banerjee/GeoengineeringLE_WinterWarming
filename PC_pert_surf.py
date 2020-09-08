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
import EOF_defs2

# user modules
import ensemble_functions
import custom_colors as ccol
#from control_NAO_EOF import eof1, PCbase, clim

#*********************************************************************************
# inputs
season = 'DJF'
varcode='PSL'
save=True

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*************************************************************************************
# load EOF, PC and control climatology
eof1 = np.load(npydir+'NAO-'+varcode+'_EOF_'+season+'.npy')
PCbase = np.load(npydir+'NAO-'+varcode+'_PCbase_'+season+'.npy')
clim = np.load(npydir+'NAO-'+varcode+'_clim_'+season+'.npy')

#*************************************************************************************
for i in range(1,21):
   print('Feedback run ',i)
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0] 

   # preprocess
   npvar, nptime, nplat, nplon, coslat = EOF_defs2.preprocess(filename, varcode, 2020, 2095)

   # anomalies from Base monthly climatology, seasonal mean
   anom = EOF_defs2.calc_anom(npvar, clim, season)

   # area subset
   anomsub, nplatsub, nplonsub, coslatsub = EOF_defs2.area_subset(anom, 'NAO', nplat, nplon, coslat)

   # projection 
   PCfeedback = EOF_defs2.projection(anomsub, eof1, PCbase)

   # save projection
   np.save(npydir+'NAO-'+varcode+'_PC_feedback_'+str(i)+'_'+season+'.npy', PCfeedback) 

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

