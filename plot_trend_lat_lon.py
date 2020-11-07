'''
Trend figure presets for sea level pressure, temperature and precipitation in publication.
Used for the RCP8.5 and geoengineering (Feedback) simulations.
Plotting both ensemble mean and individual ensemble members.
'''

# user imports
import ensemble_functions
import plot_functions
import trend_defs

#********************************************************************************************************
run = 'feedback'
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'TREFHT'
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

colorscale= {'TREFHT'  :'BlueRed',\
             'precip'  :'BrownGreen',\
             'PSL'     :'BlueRed'}

clabel    = {'TREFHT'  :'$^{\circ}$C per 30 yrs',\
             'precip'  :'mm/day per 30 yrs',\
             'PSL'     :'hPa per 30 yrs'}

#********************************************************************************************************
# Ensemble stats
members = trend_defs.trend_lat_lon(run,season,varcode)
nmembers = len(members)
ensmean, ensstd= ensemble_functions.stats(members) 
ttest = ensemble_functions.t_test_onesample(alpha, ensmean, ensstd, nmembers) 

# Plot ensemble mean
plot_functions.plot_single_lat_lon(ensmean, ensmean['lat'], ensmean['lon'],\
                                   plotlett[varcode][run][season]+' '+runname[run]+'\n'+longtitle[varcode]+'\n'+season,\
                                   outdir+varcode+'_trend_'+run+'_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1],\
                                   contours[varcode][run][0], contours[varcode][run][1],\
                                   clabel[varcode],\
                                   zsig=ttest,\
                                   colorscale=colorscale[varcode])

# Plot members 
plot_functions.plot_matrix_lat_lon(members, ensmean['lat'], ensmean['lon'],\
                                   '',\
                                   outdir+varcode+'_trend_'+run+'_members_'+season+'.png',\
                                   shading[varcode][run][0], shading[varcode][run][1],\
				   contours[varcode][run][0], contours[varcode][run][1],\
                                   clabel[varcode],\
                                   colorscale=colorscale[varcode])

#********************************************************************************************************
# END
#********************************************************************************************************
