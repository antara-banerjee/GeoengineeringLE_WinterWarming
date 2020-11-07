'''
Plot trends in variables that are congruent with the Northern Annular Mode at 50hPa (NAM50)
and the residual trends that cannot be explained by NAM50.
'''

# standard imports
import glob 
import numpy as np
import scipy.stats as ss

# user imports
import ensemble_functions
import plot_functions
import vartimeproc 

#********************************************************************************************************
season = 'DJF'
varcode = 'precip'
alpha = 0.05

npydir = "/Users/abanerjee/scripts/glens/npy_output/"
outdir="/Users/abanerjee/scripts/glens/output/"

nplevel = np.load(npydir+'nplevel.npy')

#********************************************************************************************************
# presets for paper
longtitle = {'TREFHT'  :'Temperature',\
             'precip'  :'Precipitation',\
             'PSL'     :'Sea level pressure'}

plotlett  = {'congr':{'TREFHT':'(d)','precip':'(g)','PSL':'(a)'},\
             'resid':{'TREFHT':'(f)','precip':'(i)','PSL':'(c)'}}

shading   = {'TREFHT'  :(2,0.2),\
             'precip'  :(0.4,0.05),\
             'PSL'     :(1.6,0.2)}

contours  = {'TREFHT'  :(2,0.4),\
             'precip'  :(0.4,0.1),\
             'PSL'     :(1.6,0.4)}

colorscale= {'TREFHT'  :'BlueRed',\
             'precip'  :'BrownGreen',\
             'PSL'     :'BlueRed'}

clabel    = {'TREFHT'  :'$^{\circ}$C per 30 yrs',\
             'precip'  :'mm/day per 30 yrs',\
             'PSL'     :'hPa per 30 yrs'}

#********************************************************************************************************
members_congr = []
members_resid = []
scaler = {'TREFHT':1, 'precip':1, 'PSL':0.01}
for i in range(1,21):
   
   print('Feedback run ',str(i))

   # surface response: timeseries and trend 
   if varcode=='precip':
      ncpath1 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.PRECC.202001-*.nc")[0]
      ncpath2 = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.PRECL.202001-*.nc")[0]
      vartimeobj = vartimeproc.PrecipTimeProc(ncpath1, ncpath2, tim1=2020, tim2=2095, ppt1='PRECC', ppt2='PRECL')
   else:
      ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+varcode+".202001-*.nc")[0]
      vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2020, tim2=2095, varcode=varcode)
   tseries_surf = vartimeobj.annual_mean(season)*scaler[varcode]
   trend_surf = vartimeobj.trend_lat_lon(season)*scaler[varcode]

   # NAM index at 50hPa: timeseries and trend
   ilev = np.where(nplevel==50)[0][0]
   tseries_NAM = np.load(npydir+'NAM-Z3_PC_feedback_'+str(i)+'_DJF.npy')[:,ilev]
   nyrs = tseries_NAM.shape[0]
   trend_NAM = ss.linregress(range(nyrs), tseries_NAM)[0] * 30

   # congruent trend
   regress = lambda x: ss.linregress(tseries_NAM, x)[0] * trend_NAM
   tseries_surf_flat = tseries_surf.values.reshape([tseries_surf.shape[0], tseries_surf.shape[1]*tseries_surf.shape[2]])
   congr = np.apply_along_axis(regress, 0, tseries_surf_flat).reshape([tseries_surf.shape[1],tseries_surf.shape[2]])
   resid = trend_surf.values - congr 

   members_congr.append(congr)
   members_resid.append(resid)

print("...done calculation for each member")

#ensmean_congr, ensstd_congr = ensemble_functions.stats(members_congr) 
#ensmean_resid, ensstd_resid = ensemble_functions.stats(members_resid) 

ensmean_congr = np.array(members_congr).mean(axis=0)
ensmean_resid = np.array(members_resid).mean(axis=0)
print('ensemble mean congr shape: ',ensmean_congr.shape)
print('ensemble mean resid shape: ',ensmean_resid.shape)

#********************************************************************************************************
# Plot
# congruent
plot_functions.plot_single_lat_lon(ensmean_congr, tseries_surf['lat'], tseries_surf['lon'],\
				   plotlett['congr'][varcode]+' GEO8.5: NAM$_{50}$-congruent\n'+longtitle[varcode],\
				   outdir+varcode+'_congr_feedback_'+season+'.png',\
				   shading[varcode][0], shading[varcode][1],\
				   contours[varcode][0], contours[varcode][1],\
				   clabel[varcode], colorscale=colorscale[varcode])

# residual
plot_functions.plot_single_lat_lon(ensmean_resid, tseries_surf['lat'], tseries_surf['lon'],\
				   plotlett['resid'][varcode]+' GEO8.5: Residual\n'+longtitle[varcode],\
				   outdir+varcode+'_resid_feedback_'+season+'.png',\
				   shading[varcode][0], shading[varcode][1],\
				   contours[varcode][0], contours[varcode][1],\
				   clabel[varcode], colorscale=colorscale[varcode])

#********************************************************************************************************
# END #
#********************************************************************************************************
