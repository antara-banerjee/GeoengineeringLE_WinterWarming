import glob
import xarray as xr
import matplotlib as mpl
mpl.use('Agg')
import zonal_wind
import ensemble_functions
import plot_functions

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
var = "U"
alpha = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

#********************************************************************************************************
# control climatology
print("Calculating climatology for control")

members_control = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+var+".201001-*.nc")[0]
   print(ncpath)
   U_inst = zonal_wind.zmzw(ncpath, tim1=2010, tim2=2030, var='U')
   clim_lon_lat = U_inst.climatology_lon_lat(season)
   members_control.append(clim_lon_lat)

ncontrol = len(members_control)
ensmean_control, ensstd_control = ensemble_functions.stats(members_control)

#********************************************************************************************************
# RCP8.5
# only 3 members here!
print("Calculating climatology for RCP8.5")

members_rcp85 = []
for i in [1,2,3,21]:
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0zm."+var+".201001-*.nc")[0]
   print(ncpath)
   U_inst = zonal_wind.zmzw(ncpath, tim1=2020, tim2=2095, var='U')
   trend_lon_lat = U_inst.trend_lon_lat(season)
   members_rcp85.append(trend_lon_lat)

nrcp85 = len(members_rcp85)
ensmean_rcp85, ensstd_rcp85 = ensemble_functions.stats(members_rcp85)
ttest_rcp85 = ensemble_functions.t_test_onesample(alpha, ensmean_rcp85, ensstd_rcp85, nrcp85) 

plot_functions.plot_single_lat_hgt(ensmean_rcp85, ensmean_control, '(b) RCP8.5', outdir+'U_trend_rcp85_'+season+'.png', 5, 0.5, 60, 10, 'm s$^{-1}$ per 30 yrs', zsig=ttest_rcp85)

#********************************************************************************************************
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/p.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0zm."+var+".202001-*.nc")[0]
   U_inst = zonal_wind.zmzw(ncpath, tim1=2020, tim2=2095, var='U')
   trend_lon_lat = U_inst.trend_lon_lat(season)
   members_feedback.append(trend_lon_lat)

nfeedback = len(members_feedback)
ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback)
ttest_feedback = ensemble_functions.t_test_onesample(alpha, ensmean_feedback, ensstd_feedback, nfeedback) 

plot_functions.plot_single_lat_hgt(ensmean_feedback, ensmean_control, '(a) Feedback', outdir+'U_trend_feedback_'+season+'.png', 5, 0.5, 60, 10, 'm s$^{-1}$ per 30 yrs', zsig=ttest_feedback)
#********************************************************************************************************

##********************************************************************************************************
#paths_feedback = []
#for i in range(1,21):
#   for j in range(2,10): 
#      ncpath = "/dx03/ab4283/GLENS/feedback/U/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.U.20"+str(j)+"001-20"+str(j)+"912.nc"
#      lon, lat, var_block = zonal_wind.extract_var(ncpath, xlonname='lon', xlatname='lat', xtimname='time', varname='U')
#      print var_block.shape
#   #var_tseries = 
#   #var_feedback.append(var_tseries)
