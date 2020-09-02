import glob
import xarray as xr
import vartimeproc 
import ensemble_functions
import plot_functions

#********************************************************************************************************
run = 'feedback'
season = 'JJA'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'precip'
alpha = 0.05

#********************************************************************************************************
# presets for paper
runname   = {'rcp85'   : 'RCP8.5',\
             'feedback': 'GEO8.5'}

longtitle = {'TREFHT'  :'Temperature',\
             'precip'  :'Precipitation',\
             'PSL'     :'Sea level pressure'}

plotlett  = {'TREFHT'  :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)','JJA':'(b)'}},\
             'precip'  :{'rcp85':{'DJF':'(f)'},'feedback':{'DJF':'(d)','JJA':'(e)'}},\
             'PSL'     :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)','JJA':'(b)'}}}

shading   = {'TREFHT'  :{'rcp85':(8,1), 'feedback':(2,0.2)},\
             'precip'  :{'rcp85':(0.4,0.05), 'feedback':(0.4,0.05)},\
             'PSL'     :{'rcp85':(1.6,0.2), 'feedback':(1.6,0.2)}}

contours  = {'TREFHT'  :{'rcp85':(8,1), 'feedback':(2,0.4)},\
             'precip'  :{'rcp85':(0.4,0.1), 'feedback':(0.4,0.1)},\
             'PSL'     :{'rcp85':(1.6,0.4), 'feedback':(1.6,0.4)}}

colorscale= {'TREFHT'  :'matlab',\
             'precip'  :'precip',\
             'PSL'     :'matlab'}

clabel    = {'TREFHT'  :'$^{\circ}$C per 30 yrs',\
             'precip'  :'mm/day per 30 yrs',\
             'PSL'     :'hPa per 30 yrs'}

#********************************************************************************************************
# Calculate trend for each member 
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

print("...done")

# Convert to hPa for PSL 
if varcode=='PSL':
   members = [x*0.01 for x in members]

# Ensemble stats
nmembers = len(members)
ensmean, ensstd= ensemble_functions.stats(members) 
ttest = ensemble_functions.t_test_onesample(alpha, ensmean, ensstd, nmembers) 

# Plot ensemble mean
plot_functions.plot_single_lat_lon(ensmean, ensmean['lat'], ensmean['lon'],\
                                   plotlett[varcode][run][season]+' '+runname[run]+'\n'+longtitle[varcode]+'\n'+season,\
                                   outdir+varcode+'_trend_'+run+'_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1], contours[varcode][run][0], contours[varcode][run][1],\
                                   clabel[varcode],\
                                   zsig=ttest,\
                                   colorscale=colorscale[varcode])

# Plot members 
'''
plot_functions.plot_matrix_lat_lon(members, ensmean['lat'], ensmean['lon'],\
                                   '',\
                                   outdir+varcode+'_trend_'+run+'_members_'+season+'.png',\
                                   shading[run][varcode][0], shading[run][varcode][1], contours[run][varcode][0], contours[run][varcode][1],\
                                   clabel[varcode])
'''

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
