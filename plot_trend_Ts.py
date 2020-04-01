import glob
import matplotlib as mpl
mpl.use('Agg')
#plt.ioff()
# mpl_toolkits contain the class Basemap and other functions such
# as addcyclic, shiftgrid etc.
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
'''
# control 
print("Calculating climatology for CONTROL")

members_control = []
for i in range(1,22):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, time0=2010, tim1=2010, tim2=2030)
   #clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   trend_lon_lat = Ts_inst.trend_lon_lat(season)
   members_control.append(trend_lon_lat)

print("...done")

#********************************************************************************************************
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
'''

#********************************************************************************************************
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,22):
   #ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   ncpath = glob.glob("/Volumes/Data-Banerjee/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, tim1=2020, tim2=2095, var='TREFHT')
   trend_lon_lat = Ts_inst.trend_lon_lat(season)
   members_feedback.append(trend_lon_lat)

print("...done")

#********************************************************************************************************
# ensemble statistics
'''
# number
ncontrol = len(members_control)
nrcp85 = len(members_rcp85)
'''
nfeedback = len(members_feedback)

'''
# mean and stdev
ensmean_rcp85, ensstd_rcp85 = ensemble_functions.stats(members_rcp85) 
ensmean_control, ensstd_control = ensemble_functions.stats(members_control) 
'''
ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback) 

'''
# differences
ensdiff_rcp85 = ensmean_rcp85 - ensmean_control
ensdiff_feedback = ensmean_feedback - ensmean_control

# two-tailed t-test
ttest_rcp85 = ensemble_functions.t_test(p_value, ensdiff_rcp85, ensstd_control, ensstd_rcp85, ncontrol, nrcp85) 
ttest_feedback = ensemble_functions.t_test(p_value, ensdiff_feedback, ensstd_control, ensstd_feedback, ncontrol, nfeedback) 
'''

# one-tailed t-test
ttest_feedback = ensemble_functions.t_test_onesample(alpha, ensmean_feedback, ensstd_feedback, nfeedback) 
print(ttest_feedback)

# individual member differences
#memdiff_rcp85 = [x - ensmean_control for x in members_rcp85]
#memdiff_feedback = [x - ensmean_control for x in members_feedback]

#********************************************************************************************************
# Plot ensemble mean difference FEEDBACK-CONTROL
#print(lat.shape, lon.shape)
#zsigones = np.ones([lat.shape[0],lon.shape[0]])

print("Plotting ensemble mean trend FEEDBACK")
plot_functions.plot_single_lat_lon(ensmean_feedback, 'Feedback ('+season+')', outdir+'Ts_trend_feedback_'+season+'.png', 2, 0.2, 2, 0.4, '$^{\circ}$C per 30 yrs', zsig=ttest_feedback)

#********************************************************************************************************
