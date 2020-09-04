import glob
import xarray as xr
import vartimeproc 
import ensemble_functions
import plot_functions
import clim_defs

#********************************************************************************************************
run = 'geoheats'
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'U'
alpha = 0.05

#********************************************************************************************************
# presets for paper
runname   = {'rcp85'   : 'RCP8.5',\
             'feedback': 'GEO8.5',\
             'geoheats': 'GEOHEAT'}

plotlett  = {'U'       :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'},'geoheats':{'DJF':'(b)'}}}

shading   = {'U'       :{'rcp85':(5,0.5), 'feedback':(5,0.5), 'geoheats':(5,0.5)}}

contours  = {'U'       :{'rcp85':(60,10), 'feedback':(60,10), 'geoheats':(60,10)}}

clabel    = {'U'       :'Zonal mean zonal wind (ms$^{-1}$ per 30 yrs)'}

#********************************************************************************************************
# Control climatology
members_control = clim_defs.clim_lat_hgt('control',season,varcode)
nmembers_control = len(members_control)
ensmean_control, ensstd_control = ensemble_functions.stats(members_control)

# Perturbation climatology 
members = clim_defs.clim_lat_hgt(run,season,varcode)
nmembers = len(members)
ensmean, ensstd= ensemble_functions.stats(members) 

# Difference to Base
ensdiff = ensmean - ensmean_control
ttest = ensemble_functions.t_test_twosample(alpha, ensdiff, ensstd_control, ensstd, nmembers_control, nmembers)

# Convert to trend
ensdiff = ensdiff/65.*30.

# Plot ensemble mean
plot_functions.plot_single_lat_hgt(ensdiff, ensmean_control,\
                                   plotlett[varcode][run][season]+' '+runname[run],\
                                   outdir+varcode+'_clim_'+run+'_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1], contours[varcode][run][0], contours[varcode][run][1],\
                                   clabel[varcode],\
                                   zsig=ttest)

# Plot members 
'''
plot_functions.plot_matrix_lat_hgt(members, ensmean_control,\
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
