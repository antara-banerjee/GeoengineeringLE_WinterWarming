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
import EOF_defs2

#*********************************************************************************
# inputs
season = 'DJF'
mode='NAO'
varcode='U'

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

# load saved EOF calculated from NAM_zm_all_months.py
#*************************************************************************************
eof1 = np.load('/Users/abanerjee/scripts/glens/npy_output/'+mode+'-'+varcode+'_vertical_EOF_'+season+'.npy')
PCbase = np.load('/Users/abanerjee/scripts/glens/npy_output/'+mode+'-'+varcode+'_vertical_PCbase_'+season+'.npy')
clim = np.load('/Users/abanerjee/scripts/glens/npy_output/'+mode+'-'+varcode+'_vertical_clim_'+season+'.npy')

#*********************************************************************************
nRun = 20
for run in range(1, nRun+1):
   print('Run ',run)
   filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(run).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(run).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0] 

   # preprocess
   npvar, nptime, nplev, nplat, nplon, coslat = EOF_defs2.preprocess(filename, varcode, 2020, 2095, vertical=True)
   print(npvar.shape)

   ntime = len(nptime)
   nlat  = len(nplat)
   nlon  = len(nplon)
   nlev  = len(nplev)  # additional to surface script
   PCPert = np.empty([int(ntime/12),nlev]) 

   for ilev in range(nlev):

      print('level: ', ilev, nplev[ilev])
      x = npvar[:,ilev,:,:]

      # anomalies from Base monthly climatology, seasonal mean
      anom = EOF_defs2.calc_anom(x, clim[:,ilev,:,:], season)

      # area subset
      anomsub, nplatsub, nplonsub, coslatsub = EOF_defs2.area_subset(anom, 'NAO', nplat, nplon, coslat)

      # projection 
      PC = EOF_defs2.projection(anomsub, eof1[ilev,:,:], PCbase[:,ilev])
      
      PCPert[:,ilev] = PC

   # save projection
   np.save(npydir+'NAO-'+varcode+'_PCpert_'+str(run)+'_'+season+'.npy', PCPert) 

#*************************************************************************************
# END #
#*************************************************************************************
