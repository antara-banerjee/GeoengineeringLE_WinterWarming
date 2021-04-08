'''
Setting up file paths to output from the Base, RCP8.5, Feedback and GEOHEAT_S simulations.
Calculates climatologies over chosen time period, season and variable after
instantiating the VarTimeProc class.
'''

# user imports
import ensemble_defs
import glob
import vartimeproc 

#********************************************************************************************************
def clim_lat_lon(run, season, varcode):

   members = []

   # Control climatology
   if run=='control':
      print("Calculating climatology for Control")
      
      for i in range(1,21):
         if varcode=='precip':
            ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.PRECC.201001-*.nc")[0]
            ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.PRECL.201001-*.nc")[0]
            vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=2010, tim2=2030, ppt1='PRECC', ppt2='PRECL')
         else:
            ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2010, tim2=2030, varcode=varcode)
         clim = vartimeobj.clim_mean(season)
         members.append(clim)
      
   # RCP8.5
   if run=='rcp85':
      print("Calculating climatology for RCP8.5")
      for i in [1,2,3]:
         # Precip
         if varcode=='precip':
            ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.PRECC.201001-*.nc")[0]
            ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.PRECL.201001-*.nc")[0]
            vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=2075, tim2=2095, ppt1='PRECC', ppt2='PRECL')
         # All other variables
         else:
            ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2075, tim2=2095, varcode=varcode)
         clim = vartimeobj.clim_mean(season)
         members.append(clim)
   
   # Feedback
   elif run=='feedback':
      print("Calculating climatology for Feedback")
      for i in range(1,21):
         # Precip
         if varcode=='precip':
            ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.PRECC.202001-*.nc")[0]
            ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.PRECL.202001-*.nc")[0]
            vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=2075, tim2=2095, ppt1='PRECC', ppt2='PRECL')
         # All other variables
         else:
            ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2075, tim2=2095, varcode=varcode)
         clim = vartimeobj.clim_mean(season)
         members.append(clim)
   
   # GEOHEAT_S
   elif run=='geoheats':
      print("Calculating climatology for GEOHEAT_S")
      for i in range(1,5):
         yrvals = []
         for yr in range(2011,2031):
            # Precip
            if varcode=='precip':
               ncpath1 = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/PRECC.b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
               ncpath2 = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/PRECL.b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
               vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=yr, tim2=yr+1, ppt1='PRECC', ppt2='PRECL')
            # All other variables
            else:
               ncpath = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+varcode+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
               vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=yr, tim2=yr+1, varcode=varcode)
            clim = vartimeobj.clim_mean(season)
            yrvals.append(clim)
         yrvals_mean, yrvals_std = ensemble_defs.stats(yrvals)
         members.append(yrvals_mean)

   # Convert to hPa for PSL 
   if varcode=='PSL':
      members = [x*0.01 for x in members]

   return members

#********************************************************************************************************
def clim_lat_hgt(run, season, varcode):

   members = []

   # Control Climatology
   if run=='control':
      print("Calculating climatology for control")
      
      for i in range(1,21):
         ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".201001-*.nc")[0]
         vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2010, tim2=2030, varcode=varcode, zm=True)
         clim = vartimeobj.clim_mean(season)
         members.append(clim)
   
   # RCP8.5
   if run=='rcp85':
      print("Calculating trend for RCP8.5")
      for i in [1,2,3]:
         ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".201001-*.nc")[0]
         vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2075, tim2=2095, varcode=varcode, zm=True)
         clim = vartimeobj.clim_mean(season)
         members.append(clim)

   # Feedback
   elif run=='feedback':
      print("Calculating trend for Feedback")
      for i in range(1,21):
         ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".202001-*.nc")[0]
         vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2075, tim2=2095, varcode=varcode, zm=True)
         clim = vartimeobj.clim_mean(season)
         members.append(clim)

   # GEOHEAT_S
   elif run=='geoheats':
      print("Calculating trend for GEOHEAT_S")
      for i in range(1,5):
         yrvals = []
         for yr in range(2011,2031):
            ncpath = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+varcode+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".zm.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=yr, tim2=yr+1, varcode=varcode, zm=True)
            clim = vartimeobj.clim_mean(season)
            yrvals.append(clim)
         yrvals_mean, yrvals_std = ensemble_defs.stats(yrvals)
         members.append(yrvals_mean)

   return members

print("...done")

#********************************************************************************************************
# END
#********************************************************************************************************
