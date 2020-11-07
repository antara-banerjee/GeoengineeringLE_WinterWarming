'''
Compute first Principal Component (PC) in RCP8.5, geoengineering (Feedback) and GEOHEAT_S simulations.

-Uses pre-computed EOFs derived from Base runs (use EOF_base_surf.py).
-Computed for a surface level field. 
-Mode can be NAM or NAO based on e.g. sea level pressure.
'''

# standard imports
import glob
import numpy as np

# user imports 
import PCA_defs 

#*********************************************************************************
# inputs
run = 'feedback'
season = 'JJA'
varcode = 'PSL'
save = True

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*************************************************************************************
# load EOF, PC and control climatology
eof1 = np.load(npydir+'NAO-'+varcode+'_EOF_'+season+'.npy')
PCbase = np.load(npydir+'NAO-'+varcode+'_PCbase_'+season+'.npy')
clim = np.load(npydir+'NAO-'+varcode+'_clim_'+season+'.npy')

#*************************************************************************************
if run=='feedback':
   for i in range(1,21):
      print('Feedback run ',i)

      filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0] 
   
      # preprocess
      npvar, nptime, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, 2020, 2095)
   
      # anomalies from Base monthly climatology, seasonal mean
      anom = PCA_defs.calc_anom(npvar, clim, season)
   
      # area subset
      anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, 'NAO', nplat, nplon, coslat)
   
      # projection 
      PCpert = PCA_defs.projection(anomsub, eof1, PCbase)
   
      # save projection
      np.save(npydir+'NAO-'+varcode+'_PC_feedback_'+str(i)+'_'+season+'.npy', PCpert) 

elif run=='rcp85':
   for i in range(1,4):
      print('RCP8.5 run ',i)

      filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0] 
   
      # preprocess
      npvar, nptime, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, 2020, 2095)
   
      # anomalies from Base monthly climatology, seasonal mean
      anom = PCA_defs.calc_anom(npvar, clim, season)
   
      # area subset
      anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, 'NAO', nplat, nplon, coslat)
   
      # projection 
      PCpert = PCA_defs.projection(anomsub, eof1, PCbase)
   
      # save projection
      np.save(npydir+'NAO-'+varcode+'_PC_rcp85_'+str(i)+'_'+season+'.npy', PCpert) 

elif run=='geoheats':

   for i in range(1,5):

      print('GEOHEAT_S run ',i)
      PCgeoheats = []

      for yr in range(2011,2031):

         filename = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+varcode+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]

         # preprocess
         npvar, nptime, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, yr, yr+1)
   
         # anomalies from Base monthly climatology, seasonal mean
         anom = PCA_defs.calc_anom(npvar, clim, season)
   
         # area subset
         anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, 'NAO', nplat, nplon, coslat)
   
         # projection 
         PCpert = PCA_defs.projection(anomsub, eof1, PCbase)

         PCgeoheats.append(PCpert)

      # save projection (one for each member)
      member_mean = np.array(PCgeoheats).mean(axis=0) 
      np.save(npydir+'NAO-'+varcode+'_PC_geoheats_'+str(i)+'_'+season+'.npy', member_mean)

#*************************************************************************************
# END #
#*************************************************************************************
