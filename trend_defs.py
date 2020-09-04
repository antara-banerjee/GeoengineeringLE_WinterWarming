import glob
import xarray as xr
import vartimeproc 
import ensemble_functions

#********************************************************************************************************
def trend_lat_lon(run, season, varcode):

   members = []

   # RCP8.5
   if run=='rcp85':
      print("Calculating climatology for RCP8.5")
      for i in [1,2,3]:
         # Precip
         if varcode=='precip':
            ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.PRECC.201001-*.nc")[0]
            ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.PRECL.201001-*.nc")[0]
            vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=2020, tim2=2095, ppt1='PRECC', ppt2='PRECL')
         # All other variables
         else:
            ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode)
         trend = vartimeobj.trend_lat_lon(season)
         members.append(trend)
   
   # Feedback
   elif run=='feedback':
      print("Calculating climatology for Feedback")
      for i in range(1,21):
         # Precip
         if varcode=='precip':
            ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.PRECC.202001-*.nc")[0]
            ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.PRECL.202001-*.nc")[0]
            vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=2020, tim2=2095, ppt1='PRECC', ppt2='PRECL')
         # All other variables
         else:
            ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode)
         trend = vartimeobj.trend_lat_lon(season)
         members.append(trend)
   
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
            trend = vartimeobj.trend_lat_lon(season)
            yrvals.append(trend)
         yrvals_mean, yrvals_std = ensemble_functions.stats(yrvals)
         members.append(yrvals_mean)

   # Convert to hPa for PSL 
   if varcode=='PSL':
      members = [x*0.01 for x in members]

   return members

#********************************************************************************************************
def trend_lat_hgt(run, season, varcode):

   members = []
   
   # RCP8.5
   if run=='rcp85':
      print("Calculating trend for RCP8.5")
      for i in [1,2,3]:
         ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".201001-*.nc")[0]
         vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode, zm=True)
         trend = vartimeobj.trend_lat_hgt(season)
         members.append(trend)

   # Feedback
   elif run=='feedback':
      print("Calculating trend for Feedback")
      for i in range(1,21):
         ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0zm."+varcode+".202001-*.nc")[0]
         vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode, zm=True)
         trend = vartimeobj.trend_lat_hgt(season)
         members.append(trend)

   # GEOHEAT_S
   elif run=='geoheats':
      print("Calculating trend for GEOHEAT_S")
      for i in range(1,5):
         yrvals = []
         for yr in range(2011,2031):
            ncpath = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+varcode+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".zm.nc")[0]
            vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=yr, tim2=yr+1, varcode=varcode, zm=True)
            trend = vartimeobj.trend_lat_hgt(season)
            yrvals.append(trend)
         yrvals_mean, yrvals_std = ensemble_functions.stats(yrvals)
         members.append(yrvals_mean)

   return members

print("...done")

#********************************************************************************************************
# END
#********************************************************************************************************

'''
t = xr.open_dataset('xrToE_Ts_trend_2stdev.nc')
#t = t.where(ttest_feedback==0)
plot_functions.plot_ToE(t.__xarray_dataarray_variable__,'ToE','ToE_Ts_trend_2stdev.png',2020,2095,5,'year')

t = xr.open_dataset('xrToE_Ts_clim_2stdev_stdcontrol.nc')
print(t.__xarray_dataarray_variable__[0,:])
plot_functions.plot_ToE(t.__xarray_dataarray_variable__,'ToE','ToE_2stdev_stdcontrol.png',2020,2095,5,'year')
#plot_functions.plot_ToE(t.__xarray_dataarray_variable__[:,:,-1],'ToE','ToE_2stdev_stdcontrol.png',0,1,0.1,'year')
'''

#********************************************************************************************************
