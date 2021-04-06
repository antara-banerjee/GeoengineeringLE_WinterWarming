'''
Trend figure presets for zonal mean zonal wind in publication.
Used for the RCP8.5 and geoengineering (Feedback) simulations.
Plotting both ensemble mean and individual ensemble members.
'''

# standard functions
import numpy as np
import xarray as xr

# user functions
import clim_defs
import ensemble_functions
import plot_functions
import trend_defs

#********************************************************************************************************
run = 'feedback'
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'T'
alpha = 0.05

#********************************************************************************************************
# presets for paper
runname   = {'rcp85'   : 'RCP8.5',\
             'feedback': 'GEO8.5'}

plotlett  = {'U'       :{'rcp85':{'DJF':'(f)'},'feedback':{'DJF':'(d)'}},\
            'T'       :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'}}}

shading   = {'U'       :{'rcp85':(5,0.5), 'feedback':(5,0.5)},\
            'T'       :{'rcp85':(5,0.5), 'feedback':(5,0.5)}}

cbar      = {'U'       :{'rcp85':(5,1), 'feedback':(5,1)},\
            'T'       :{'rcp85':(5,1), 'feedback':(5,1)}}

contours  = {'U'       :{'rcp85':(60,10), 'feedback':(60,10)},\
            'T'       :{'rcp85':(300,10), 'feedback':(300,10)}}

cdp       = {'U'       :{'rcp85':0, 'feedback':0},\
            'T'       :{'rcp85':0, 'feedback':0}}

clabel    = {'U'       :'Zonal mean zonal wind (ms$^{-1}$ per 30 yrs)',\
            'T'       :'Temperature ($^{\circ}$C per 30 yrs)'}

#********************************************************************************************************
# Control climatology
members_control = clim_defs.clim_lat_hgt('control',season,varcode)
nmembers_control = len(members_control)
ensmean_control, ensstd_control = ensemble_functions.stats(members_control)

# Perturbation climatology 
members = trend_defs.trend_lat_hgt(run,season,varcode)
nmembers = len(members)
ensmean, ensstd = ensemble_functions.stats(members) 
ttest = ensemble_functions.t_test_onesample(alpha, ensmean, ensstd, nmembers) 

areawgt = np.cos(np.deg2rad(ensmean.lat))
#ensmean_weighted = ensmean.weighted(areawgt)
T50trop = (ensmean.sel(lat=slice(-30,30),level=50)*areawgt.sel(lat=slice(-30,30))).sum() / areawgt.sel(lat=slice(-30,30)).sum()
T50pole = (ensmean.sel(lat=slice(60,90),level=50)*areawgt.sel(lat=slice(60,90))).sum() / areawgt.sel(lat=slice(60,90)).sum()
print(round(T50trop - T50pole),2))

'''
# Plot ensemble mean
plot_functions.plot_single_lat_hgt(ensmean, ensmean_control,\
                                   plotlett[varcode][run][season]+' '+runname[run],\
                                   outdir+varcode+'_trend_'+run+'_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1],\
                                   cbar[varcode][run][0], cbar[varcode][run][1],\
				   contours[varcode][run][0], contours[varcode][run][1],\
			           cdp[varcode][run],\
                                   clabel[varcode],\
                                   zsig=ttest)
'''

# Plot members 
plot_functions.plot_matrix_lat_hgt(members, ensmean_control, ensmean_control['lat'], ensmean_control['level'],\
                                   '',\
                                   outdir+varcode+'_trend_'+run+'_members_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1],\
                                   cbar[varcode][run][0], cbar[varcode][run][1],\
				   contours[varcode][run][0], contours[varcode][run][1],\
                                   clabel[varcode])

'''
plot_functions.plot_single_lat_hgt(ensmean, ensmean,\
				   runname[run],\
                                   outdir+varcode+'_trend_'+run+'_'+season+'.png',\
                                   10, 1, 10, 1, 10, 1, 1, 'T / degreesC',\
				   zsig=ttest) 
'''

#********************************************************************************************************
# END
#********************************************************************************************************
