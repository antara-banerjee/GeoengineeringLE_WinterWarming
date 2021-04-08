'''
Trend figure presets for zonal mean zonal wind in publication.
Used for the GEOHEAT run where the trend is inferred from the climatological difference to Base.
Plotting both ensemble mean and individual ensemble members.
'''

# standard imports
import numpy as np
import xarray as xr

# user imports
import clim_defs
import ensemble_defs
import plot_defs

#********************************************************************************************************
run = 'geoheats'
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'T'
alpha = 0.05

#********************************************************************************************************
# presets for paper
runname   = {'rcp85'   : 'RCP8.5',\
             'feedback': 'GEO8.5',\
             'geoheats': 'GEOHEAT'}

plotlett  = {'U'       :{'rcp85':{'DJF':'(c)','JJA':'(c)','SON':'(c)'},'feedback':{'DJF':'(a)','JJA':'(c)','SON':'(c)'},'geoheats':{'DJF':'(e)','JJA':'(c)','SON':'(c)'}}}

shading   = {'U'       :{'rcp85':(5,0.5), 'feedback':(5,0.5), 'geoheats':(5,0.5)},\
             'T'       :{'rcp85':(5,0.5), 'feedback':(5,0.5), 'geoheats':(5,0.5)}}

cbar      = {'U'       :{'rcp85':(5,1), 'feedback':(5,1), 'geoheats':(5,1)}}

contours  = {'U'       :{'rcp85':(60,10), 'feedback':(60,10), 'geoheats':(60,10)},\
             'T'       :{'rcp85':(300,10), 'feedback':(300,10), 'geoheats':(300,10)}}

cdp       = {'U'       :{'rcp85':0, 'feedback':0, 'geoheats':0}}

clabel    = {'U'       :'Zonal mean zonal wind (ms$^{-1}$ per 30 yrs)',\
             'T'       :'Temperature ($^{\circ}$C per 30 yrs)'}

plotlett['T'] = plotlett['U']
cbar['T'] = cbar['U']
cdp['T'] = cdp['U']

#********************************************************************************************************
# Control climatology
members_control = clim_defs.clim_lat_hgt('control',season,varcode)
nmembers_control = len(members_control)
ensmean_control, ensstd_control = ensemble_defs.stats(members_control)

# Perturbation climatology 
members = clim_defs.clim_lat_hgt(run,season,varcode)
nmembers = len(members)
ensmean, ensstd = ensemble_defs.stats(members) 

# Difference to Base
ensdiff = ensmean - ensmean_control
ttest = ensemble_defs.t_test_twosample(alpha, ensdiff, ensstd_control, ensstd, nmembers_control, nmembers)

# Convert to trend
ensdiff = ensdiff/65.*30.

areawgt = np.cos(np.deg2rad(ensmean.lat))
T50trop = (ensdiff.sel(lat=slice(-30,30),level=50)*areawgt.sel(lat=slice(-30,30))).sum() / areawgt.sel(lat=slice(-30,30)).sum()
T50pole = (ensdiff.sel(lat=slice(60,90),level=50)*areawgt.sel(lat=slice(60,90))).sum() / areawgt.sel(lat=slice(60,90)).sum()
print(T50trop - T50pole)

# Plot ensemble mean
plot_defs.plot_single_lat_hgt(ensdiff, ensmean_control,\
                                   plotlett[varcode][run][season]+' '+runname[run],\
                                   outdir+varcode+'_clim_'+run+'_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1],\
				   cbar[varcode][run][0], cbar[varcode][run][1],\
 				   contours[varcode][run][0], contours[varcode][run][1],\
			           cdp[varcode][run],\
                                   clabel[varcode],\
                                   zsig=ttest)

'''
# Plot members 
plot_defs.plot_matrix_lat_hgt(members, ensmean_control,\
                                   '',\
                                   outdir+varcode+'_trend_'+run+'_members_'+season+'.png',\
                                   shading[run][varcode][0], shading[run][varcode][1], contours[run][varcode][0], contours[run][varcode][1],\
                                   clabel[varcode])
'''

'''
# testing for T
# Plot ensemble mean
plot_defs.plot_single_lat_hgt_onesided(ensmean_control, ensmean_control,\
                                   'T',\
                                   #outdir+varcode+'_clim_'+run+'_'+season+'.png',\
                                   outdir+varcode+'_clim_control_'+season+'.png',\
                                   300, 10, 300, 10, 300, 10, 1,\
                                   'T',\
                                   zsig=ttest)
'''
#********************************************************************************************************
# END
#********************************************************************************************************
