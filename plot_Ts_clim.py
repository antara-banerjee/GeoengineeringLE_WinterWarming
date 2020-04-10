import glob
import matplotlib as mpl
mpl.use('Agg')
import surface_temp
import ensemble_functions
import plot_functions

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
var = "TREFHT"
alpha = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

#********************************************************************************************************

# control 
print("Calculating climatology for CONTROL")

members_control = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, tim1=2010, tim2=2030, var='TREFHT')
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
ttest_rcp85 = ensemble_functions.t_test(p_value, ensdiff_rcp85, ensstd_control, ensstd_rcp85, ncontrol, nrcp85) 

'''
#********************************************************************************************************
'''
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2020, tim1=2025, tim2=2035)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_feedback.append(clim_lon_lat)

print("...done")

nfeedback = len(members_feedback)
ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback) 
ensdiff_feedback = ensmean_feedback - ensmean_control
ttest_feedback = ensemble_functions.t_test(p_value, ensdiff_feedback, ensstd_control, ensstd_feedback, ncontrol, nfeedback)

print("Plotting ensemble mean difference FEEDBACK-CONTROL")
plot_functions.plot_single_lat_lon(ensdiff_feedback, 'Feedback (2075-2095) - Control (2010-2030)\n'+season, outdir+'Ts_ensdiff_feedback-control_'+season+'.pdf', 8, 1, 8, 1, '$^{\circ}$C', zsig=ttest_feedback)

'''
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
ttest_geoheat = ensemble_functions.t_test(p_value, ensdiff_geoheat, ensstd_control, ensstd_geoheat, ncontrol, ngeoheat) 
'''
#********************************************************************************************************
# GEOHEAT_S runs
print("Calculating climatology for GEOHEAT_S")

members_geoheatS = []
for i in range(1,4):
   for yr in range(2011,2031):
      ncpath = glob.glob("/Volumes/CESM-GLENS/SUE/"+str(i).zfill(3)+"/b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+"/Combined/TREFHT.b.e15.B5505C5WCCML45BGCR.f09_g16.GEOHEATSUE."+str(i).zfill(3)+"_"+str(yr)+".nc")[0]
      Ts_inst = surface_temp.Ts(ncpath, tim1=yr, tim2=yr+1, var='TREFHT')
      clim_lon_lat = Ts_inst.climatology_lon_lat(season)
      members_geoheatS.append(clim_lon_lat)

print("...done")

ngeoheatS = len(members_geoheatS)
ensmean_geoheatS, ensstd_geoheatS = ensemble_functions.stats(members_geoheatS)
ensdiff_geoheatS = (ensmean_geoheatS - ensmean_control) / 65.*30.
ttest_geoheatS = ensemble_functions.t_test(alpha, ensdiff_geoheatS, ensstd_control, ensstd_geoheatS, ncontrol, ngeoheatS)

print("Plotting ensemble mean difference GEOHEAT_S-CONTROL")
#plot_functions.plot_single_lat_lon(ensdiff_geoheatS, 'GEOHEAT_S (2010-2030) - Control (2010-2030)\n'+season, outdir+'Ts_ensdiff_geoheatS-control_'+season+'.png', 8, 1, 8, 1, '$^{\circ}$C', zsig=ttest_geoheatS)
plot_functions.plot_single_lat_lon(ensdiff_geoheatS, 'GEOHEAT_S (2010-2030) - Control (2010-2030)\n'+season, outdir+'Ts_ensdiff_geoheatS-control_'+season+'.png', 2, 0.2, 2, 0.2, '$^{\circ}$C per 30 yrs', zsig=ttest_geoheatS)

#********************************************************************************************************

# individual member differences
#memdiff_rcp85 = [x - ensmean_control for x in members_rcp85]
#memdiff_feedback = [x - ensmean_control for x in members_feedback]

#********************************************************************************************************
# Plot ensemble mean difference FEEDBACK-CONTROL
#print(lat.shape, lon.shape)
#zsigones = np.ones([lat.shape[0],lon.shape[0]])


#
#print("Plotting ensemble mean difference RCP8.5-CONTROL")
#plot_functions.plot_single_lat_lon(ensdiff_rcp85, 'RCP8.5 (2075-2095) - Control (2010-2030)\n'+season, outdir+'Ts_ensdiff_rcp85-control_'+season+'.png', 8, 1, '$^{\circ}$C', zsig=ttest_rcp85)

#print("Plotting ensemble mean difference GEOHEAT-CONTROL")
#plot_functions.plot_single_lat_lon(ensdiff_geoheat, 'GEOHEAT (2010-2030) - Control (2010-2030)\n'+season, outdir+'Ts_ensdiff_geoheat-control_'+season+'.png', 8, 1, 8, 1, '$^{\circ}$C', zsig=ttest_geoheat)



#print("Plotting member differences FEEDBACK-CONTROL")
#ensemble_functions.plot_matrix_lat_lon(memdiff_feedback, lat, lon, 'Feedback (2075-2095) - Control (2010-2030), '+season, outdir+'Ts_memdiff_feedback-control_'+season+'.pdf', 8, 1, '$^{\circ}$C')
#
#print("Plotting member differences RCP8.5-CONTROL")
#ensemble_functions.plot_matrix_lat_lon(memdiff_rcp85, lat, lon, 'RCP8.5 (2075-2095) - Control (2010-2030), '+season, outdir+'Ts_memdiff_rcp85-control_'+season+'.pdf', 8, 1, '$^{\circ}$C')
#********************************************************************************************************
