'''
Compute first Principal Component (PC) in RCP8.5, geoengineering (Feedback) and GEOHEAT_S simulations.

-Uses pre-computed EOFs derived from Base runs (use EOF_base_vert.py).
-Computed for each pressure level. 
-Mode can be NAM or NAO based on e.g. geopotential height or zonal wind fields.
'''

# standard imports
import glob
import numpy as np

# user imports
import PCA_defs 

#*********************************************************************************
# inputs
run = 'feedback'
season = 'DJF'
varcode = 'Z3'
mode = 'NAM'
save = True

outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*************************************************************************************
# load saved EOF calculated from NAM_zm_all_months.py
eof1 = np.load('/Users/abanerjee/scripts/glens/npy_output/'+mode+'-'+varcode+'_vertical_EOF_'+season+'.npy')
PCbase = np.load('/Users/abanerjee/scripts/glens/npy_output/'+mode+'-'+varcode+'_vertical_PCbase_'+season+'.npy')
clim = np.load('/Users/abanerjee/scripts/glens/npy_output/'+mode+'-'+varcode+'_vertical_clim_'+season+'.npy')

#*********************************************************************************
if run=='feedback':
   for i in range(1, 21):
      print('Feedback run ',i)

      filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0] 
   
      # preprocess
      npvar, nptime, nplev, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, 2020, 2095, vertical=True)
      print(npvar.shape)
   
      ntime = len(nptime)
      nlat  = len(nplat)
      nlon  = len(nplon)
      nlev  = len(nplev)  # additional to surface script
      PCPert = np.empty([int(ntime/12),nlev]) 
   
      for ilev in range(nlev):
   
         print('level: ', ilev, nplev[ilev])
         x = npvar[:,ilev,:,:]
   
         # remove global mean if using geopotential height
         if varcode=='Z3':
            x = PCA_defs.remove_gm(x, nplat, coslat)

         # anomalies from Base monthly climatology, seasonal mean
         anom = PCA_defs.calc_anom(x, clim[:,ilev,:,:], season)
   
         # area subset
         anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, mode, nplat, nplon, coslat)
   
         # projection 
         PC = PCA_defs.projection(anomsub, eof1[ilev,:,:], PCbase[:,ilev])
         
         PCPert[:,ilev] = PC
   
      # save projection
      if save==True:
         np.save(npydir+mode+'-'+varcode+'_PC_feedback_'+str(i)+'_'+season, PCPert) 

elif run=='rcp85':
   for i in range(1, 4):
      print('RCP8.5 run ',i)

      filename = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0] 
   
      # preprocess
      npvar, nptime, nplev, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, 2020, 2095, vertical=True)
      print(npvar.shape)
   
      ntime = len(nptime)
      nlat  = len(nplat)
      nlon  = len(nplon)
      nlev  = len(nplev)  # additional to surface script
      PCPert = np.empty([int(ntime/12),nlev]) 
   
      for ilev in range(nlev):
   
         print('level: ', ilev, nplev[ilev])
         x = npvar[:,ilev,:,:]
   
         # remove global mean if using geopotential height
         if varcode=='Z3':
            x = PCA_defs.remove_gm(x, nplat, coslat)

         # anomalies from Base monthly climatology, seasonal mean
         anom = PCA_defs.calc_anom(x, clim[:,ilev,:,:], season)
   
         # area subset
         anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, mode, nplat, nplon, coslat)
   
         # projection 
         PC = PCA_defs.projection(anomsub, eof1[ilev,:,:], PCbase[:,ilev])
         
         PCPert[:,ilev] = PC
   
      # save projection
      if save==True:
         np.save(npydir+mode+'-'+varcode+'_PC_rcp85_'+str(i)+'_'+season+'.npy', PCPert) 

elif run=='geoheats':

   for i in range(4, 5):

      print('GEOHEAT_S run ',i)
      PCgeoheats = []

      for yr in range(2011,2031):
         filename = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+varcode+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
   
         # preprocess
         npvar, nptime, nplev, nplat, nplon, coslat = PCA_defs.preprocess(filename, varcode, yr, yr+1, vertical=True)
         #print(npvar.shape)
   
         ntime = len(nptime)
         nlat  = len(nplat)
         nlon  = len(nplon)
         nlev  = len(nplev)  # additional to surface script
         PCPert = np.empty([int(ntime/12),nlev]) 
   
         for ilev in range(nlev):
   
            print('level: ', ilev, nplev[ilev])
            x = npvar[:,ilev,:,:]
   
            # remove global mean if using geopotential height
            if varcode=='Z3':
               x = PCA_defs.remove_gm(x, nplat, coslat)

            # anomalies from Base monthly climatology, seasonal mean
            anom = PCA_defs.calc_anom(x, clim[:,ilev,:,:], season)
   
            # area subset
            anomsub, nplatsub, nplonsub, coslatsub = PCA_defs.area_subset(anom, mode, nplat, nplon, coslat)
   
            # projection 
            PC = PCA_defs.projection(anomsub, eof1[ilev,:,:], PCbase[:,ilev])
            
            PCPert[:,ilev] = PC

         PCgeoheats.append(PCPert)
         print(np.array(PCgeoheats).shape)
   
      # save projection (one for each member)
      member_mean = np.array(PCgeoheats).mean(axis=0) 
      
      if save==True:
         np.save(npydir+mode+'-'+varcode+'_PC_geoheats_'+str(i)+'_'+season, member_mean) 

#*************************************************************************************
# END #
#*************************************************************************************
