'''
Trend figure presets for sea level pressure, temperature and precipitation in publication.
Used for the GEOHEAT run where the trend is inferred from the climatological difference to Base.
Plotting both ensemble mean and individual ensemble members.
'''

# user imports
import clim_defs 
import ensemble_functions
import plot_functions

#********************************************************************************************************
run = 'geoheats'
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

plotlett  = {'TREFHT'  :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'},'geoheats':{'DJF':'(e)'}},\
             'precip'  :{'rcp85':{'DJF':'(f)'},'feedback':{'DJF':'(d)'},'geoheats':{'DJF':'(h)'}},\
             'PSL'     :{'rcp85':{'DJF':'(c)'},'feedback':{'DJF':'(a)'},'geoheats':{'DJF':'(b)'}}}

shading   = {'TREFHT'  :{'rcp85':(8,1), 'feedback':(3.6,0.4), 'geoheats':(2,0.2)},\
             'precip'  :{'rcp85':(0.4,0.05), 'feedback':(1,0.5), 'geoheats':(0.4,0.05)},\
             'PSL'     :{'rcp85':(1.6,0.2), 'feedback':(1.6,0.2), 'geoheats':(1.6,0.2)}}

contours  = {'TREFHT'  :{'rcp85':(8,1), 'feedback':(3.6,0.4), 'geoheats':(2,0.4)},\
             'precip'  :{'rcp85':(0.4,0.1), 'feedback':(1,0.4), 'geoheats':(0.4,0.1)},\
             'PSL'     :{'rcp85':(1.6,0.4), 'feedback':(1.6,0.4), 'geoheats':(1.6,0.4)}}

colorscale= {'TREFHT'  :'BlueRed',\
             'precip'  :'BrownGreen',\
             'PSL'     :'BlueRed'}

clabel    = {'TREFHT'  :'$^{\circ}$C per 30 yrs',\
             'precip'  :'mm/day per 30 yrs',\
             'PSL'     :'hPa per 30 yrs'}

#********************************************************************************************************
# Base climatology
members_base = clim_defs.clim_lat_lon('control',season,varcode)
nmembers_base = len(members_base)
ensmean_base, ensstd_base = ensemble_functions.stats(members_base)

# Perturbation climatology 
members = clim_defs.clim_lat_lon(run,season,varcode)
nmembers = len(members)
ensmean, ensstd = ensemble_functions.stats(members) 

# Difference to Base
ensdiff = ensmean - ensmean_base
ttest = ensemble_functions.t_test_twosample(alpha, ensdiff, ensstd_base, ensstd, nmembers_base, nmembers) 

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
