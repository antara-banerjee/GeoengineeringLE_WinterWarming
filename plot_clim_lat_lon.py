import glob
import xarray as xr
import vartimeproc 
import ensemble_functions
import plot_functions
import clim_defs 

#********************************************************************************************************
run = 'rcp85'
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'precip'
alpha = 0.05

#********************************************************************************************************
# presets for paper
runname   = {'rcp85'   : 'RCP8.5',\
             'feedback': 'GEO8.5',\
             'geoheats': 'GEOHEAT'}

longtitle = {'TREFHT'  :'Temperature',\
             'precip'  :'Precipitation',\
             'PSL'     :'Sea level pressure'}

plotlett  = {'TREFHT'  :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'},'geoheats':{'DJF':'(f)'}},\
             'precip'  :{'rcp85':{'DJF':'(f)'},'feedback':{'DJF':'(d)'},'geoheats':{'DJF':'(i)'}},\
             'PSL'     :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'},'geoheats':{'DJF':'(c)'}}}

shading   = {'TREFHT'  :{'rcp85':(8,1), 'feedback':(2,0.2), 'geoheats':(2,0.2)},\
             'precip'  :{'rcp85':(0.4,0.05), 'feedback':(0.4,0.05), 'geoheats':(0.4,0.05)},\
             'PSL'     :{'rcp85':(1.6,0.2), 'feedback':(1.6,0.2), 'geoheats':(1.6,0.2)}}

contours  = {'TREFHT'  :{'rcp85':(8,1), 'feedback':(2,0.4), 'geoheats':(2,0.4)},\
             'precip'  :{'rcp85':(0.4,0.1), 'feedback':(0.4,0.1), 'geoheats':(0.4,0.1)},\
             'PSL'     :{'rcp85':(1.6,0.4), 'feedback':(1.6,0.4), 'geoheats':(1.6,0.4)}}

colorscale= {'TREFHT'  :'BlueRed',\
             'precip'  :'BrownGreen',\
             'PSL'     :'BlueRed'}

clabel    = {'TREFHT'  :'$^{\circ}$C per 30 yrs',\
             'precip'  :'mm/day per 30 yrs',\
             'PSL'     :'hPa per 30 yrs'}

#********************************************************************************************************
# Control climatology
members_control = clim_defs.clim_lat_lon('control',season,varcode)
nmembers_control = len(members_control)
ensmean_control, ensstd_control = ensemble_functions.stats(members_control)

# Perturbation climatology 
members = clim_defs.clim_lat_lon(run,season,varcode)
nmembers = len(members)
ensmean, ensstd= ensemble_functions.stats(members) 

# Difference to Base
ensdiff = ensmean - ensmean_control
ttest = ensemble_functions.t_test_twosample(alpha, ensdiff, ensstd_control, ensstd, nmembers_control, nmembers) 

# Convert to trend
ensdiff = ensdiff/65.*30.

# Plot ensemble mean
plot_functions.plot_single_lat_lon(ensdiff, ensdiff['lat'], ensdiff['lon'],\
                                   plotlett[varcode][run][season]+' '+runname[run]+'\n'+longtitle[varcode],\
                                   outdir+varcode+'_clim_'+run+'_'+season+'.png',\
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
