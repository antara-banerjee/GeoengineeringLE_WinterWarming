import glob
import matplotlib as mpl
mpl.use('Agg')
import surface_temp
import ensemble_functions
import plot_functions

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
var1 = "PRECC"
var2 = "PRECL"
alpha = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

#********************************************************************************************************

# control 
print("Calculating climatology for CONTROL")

members_control = []
for i in range(1,21):
   print(i)
   ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var1+".201001-*.nc")[0]
   ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var2+".201001-*.nc")[0]
   Ts_inst = surface_temp.ppt(ncpath1, ncpath2, tim1=2010, tim2=2030, ppt1=var1, ppt2=var2)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season) 
   members_control.append(clim_lon_lat)

print("...done")

ncontrol = len(members_control)
ensmean_control, ensstd_control = ensemble_functions.stats(members_control)
 

#********************************************************************************************************
'''
# RCP8.5
# only 3 members here!
print("Calculating climatology for RCP8.5")

members_rcp85 = []
for i in [1,2,3,21]:
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2010, tim1=2075, tim2=2095)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_rcp85.append(clim_lon_lat)

print("...done")

nrcp85 = len(members_rcp85)
ensmean_rcp85, ensstd_rcp85 = ensemble_functions.stats(members_rcp85)
ensdiff_rcp85 = ensmean_rcp85 - ensmean_control
ttest_rcp85 = ensemble_functions.t_test(alpha, ensdiff_rcp85, ensstd_control, ensstd_rcp85, ncontrol, nrcp85) 

'''
#********************************************************************************************************
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,22):
   ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var1+".202001-*.nc")[0]
   ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var2+".202001-*.nc")[0]
   Ts_inst = surface_temp.ppt(ncpath1, ncpath2, tim1=2075, tim2=2095, ppt1=var1, ppt2=var2)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_feedback.append(clim_lon_lat)

print("...done")

nfeedback = len(members_feedback)
ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback) 
ensdiff_feedback = ensmean_feedback - ensmean_control
ttest_feedback = ensemble_functions.t_test(alpha, ensdiff_feedback, ensstd_control, ensstd_feedback, ncontrol, nfeedback)

print("Plotting ensemble mean difference FEEDBACK-CONTROL")
plot_functions.plot_single_lat_lon(ensdiff_feedback/65.*30., ensdiff_feedback['lat'], ensdiff_feedback['lon'], 'Precipitation', outdir+'ppt_ensdiff_feedback-control_'+season+'.pdf', 0.4, 0.05, 0.4, 0.1, 'mm/day per 30 years', zsig=ttest_feedback)

#********************************************************************************************************
'''
# GEOHEAT runs
print("Calculating climatology for GEOHEAT")

members_geoheat = []
for i in range(3,7):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GEOHEAT/"+str(i).zfill(3)+"/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEAT.control."+str(i).zfill(3)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2010, tim1=2010, tim2=2029)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_geoheat.append(clim_lon_lat)

print("...done")

ngeoheat = len(members_geoheat)
ensmean_geoheat, ensstd_geoheat = ensemble_functions.stats(members_geoheat)
ensdiff_geoheat = ensmean_geoheat - ensmean_control 
ttest_geoheat = ensemble_functions.t_test(alpha, ensdiff_geoheat, ensstd_control, ensstd_geoheat, ncontrol, ngeoheat) 
'''
'''
#********************************************************************************************************
# GEOHEAT_S runs
print("Calculating climatology for GEOHEAT_S")

members_geoheatS = []
for i in range(1,4):
   for yr in range(2011,2031):
      print(yr)
      ncpath1 = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+var1+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
      ncpath2 = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/"+var2+".b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
      Ts_inst = surface_temp.ppt(ncpath1, ncpath2, tim1=yr, tim2=yr+1, ppt1=var1, ppt2=var2)
      clim_lon_lat = Ts_inst.climatology_lon_lat(season) 
      members_geoheatS.append(clim_lon_lat)

print("...done")

ngeoheatS = len(members_geoheatS)
ensmean_geoheatS, ensstd_geoheatS = ensemble_functions.stats(members_geoheatS)
ensdiff_geoheatS = (ensmean_geoheatS - ensmean_control)
ttest_geoheatS = ensemble_functions.t_test(alpha, ensdiff_geoheatS, ensstd_control, ensstd_geoheatS, ncontrol, ngeoheatS)

print("Plotting ensemble mean difference GEOHEAT_S-CONTROL")
plot_functions.plot_single_lat_lon(ensdiff_geoheatS / 65.*30., ensdiff_geoheatS['lat'], ensdiff_geoheatS['lon'], '(c) Precipitation', outdir+'ppt_ensdiff_geoheatS-control_'+season+'.png', 0.4, 0.05, 0.4, 0.1, 'mm/day per 30 yrs', zsig=ttest_geoheatS)
'''

#********************************************************************************************************
