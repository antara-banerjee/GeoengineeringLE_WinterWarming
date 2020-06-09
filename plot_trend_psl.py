import glob
import matplotlib as mpl
mpl.use('Agg')
#plt.ioff()
# mpl_toolkits contain the class Basemap and other functions such
# as addcyclic, shiftgrid etc.
import surface_temp
import ensemble_functions
import plot_functions
import xarray as xr

#********************************************************************************************************
season = 'SON'
outdir="/Users/abanerjee/scripts/glens/output/"
var = "PSL"
alpha = 0.05
pa_to_hpa = 0.01

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

'''
#********************************************************************************************************
# RCP8.5
# only 3 members here!
print("Calculating climatology for RCP8.5")

members_rcp85 = []
for i in [1,2,3]:
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, tim1=2010, tim2=2095, var=var)
   trend_lon_lat = Ts_inst.trend_lon_lat(season) *0.01
   members_rcp85.append(trend_lon_lat)

print("...done")

nrcp85 = len(members_rcp85)
ensmean_rcp85, ensstd_rcp85 = ensemble_functions.stats(members_rcp85); print(ensmean_rcp85)
ttest_rcp85 = ensemble_functions.t_test_onesample(alpha, ensmean_rcp85, ensstd_rcp85, nrcp85) # one-tailed t-test
plot_functions.plot_single_lat_lon(ensmean_rcp85, ensmean_rcp85['lat'], ensmean_rcp85['lon'], 'RCP8.5\nTotal', outdir+var+'_trend_rcp85_'+season+'.png', 1.6, 0.2, 1.6, 0.4, 'Sea level pressure (hPa per 30 yrs)', zsig=ttest_rcp85)
plot_functions.plot_matrix_lat_lon(members_rcp85, ensmean_rcp85['lat'], ensmean_rcp85['lon'], '', outdir+'psl_trend_rcp85_members_'+season+'.png', 1.6, 0.2, 1.6, 0.4, 'Sea level pressure (hPa per 30 yrs)')
'''

#********************************************************************************************************
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,21):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, tim1=2020, tim2=2095, var=var)
   trend_lon_lat = Ts_inst.trend_lon_lat(season) *0.01
   members_feedback.append(trend_lon_lat)

print("...done")

nfeedback = len(members_feedback)
ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback) 
ttest_feedback = ensemble_functions.t_test_onesample(alpha, ensmean_feedback, ensstd_feedback, nfeedback) # one-tailed t-test
print(ttest_feedback)
#plot_functions.plot_single_lat_lon(ensmean_feedback, ensmean_feedback['lat'], ensmean_feedback['lon'], 'Feedback\nTotal', outdir+var+'_trend_feedback_'+season+'.png', 1.6, 0.2, 1.6, 0.4, 'Sea level pressure (hPa per 30 yrs)', zsig=ttest_feedback)
plot_functions.plot_single_lat_lon(ensmean_feedback, ensmean_feedback['lat'], ensmean_feedback['lon'], '(d) '+season, outdir+var+'_trend_feedback_'+season+'.png', 1.6, 0.2, 1.6, 0.4, 'Sea level pressure (hPa per 30 yrs)', zsig=ttest_feedback)
#plot_functions.plot_matrix_lat_lon(members_feedback, ensmean_feedback['lat'], ensmean_feedback['lon'], '', outdir+'psl_trend_feedback_members_'+season+'.png', 1.6, 0.2, 1.6, 0.4, 'Sea level pressure (hPa per 30 yrs)')
'''
#*****************************************************************************************************
t = xr.open_dataset('xrToE_psl_trend_2stdev.nc')
#t = t.where(t!=2095)
#t = t.where(t!=2021)
#t = t.where(t!=0)
#t = t.where(ttest_feedback==0)
plot_functions.plot_ToE(t.__xarray_dataarray_variable__,'ToE','ToE_psl_trend_2stdev.png',2020,2095,5,'year')
'''
#*****************************************************************************************************
