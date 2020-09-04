import glob
import ensemble_functions
import plot_functions
import clim_defs 
import numpy as np
import xarray as xr
import vartimeproc

# check ensmean control mean of 21*20 is the same as mean of 21, then mean of 20 (could plot)
# check then that endsdiff is the same with the two methods
# check macmartin paper for calculation of residuals and interannual sigma (concatenate Base?)

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'TREFHT'

#********************************************************************************************************
# 1) Plot interannual sigma from Base variability
members_control = []
for i in range(1,21):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0]
   vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2010, tim2=2030, varcode=varcode)
   ann = vartimeobj.annual_mean(season)
   members_control.append(ann)

dim = 'member'
new_coord = range(len(members_control))

func = lambda *x: np.stack(x, axis=-1)
stack = xr.apply_ufunc(func, *members_control,
                     output_core_dims=[[dim]],
                     join='outer',
                     dataset_fill_value=np.nan)
stack[dim] = new_coord

# Doesn't matter if taking differences for each member from its time average 
#ensmean_control = stack.mean('time')
#ensstd_control = stack.std('time')
# Take differences from time and ensemble mean
ensmean_control = stack.mean(dim=('time','member'))
ensstd_control = stack.std(dim=('time','member'))

# interannual variability (represented by 21*20 residuals)
residuals = stack - ensmean_control
stdcontrol = residuals.std(dim=('time','member'))

plot_functions.plot_ToE(stdcontrol, ensmean_control['lat'], ensmean_control['lon'], '(b) Interannual $\sigma$', outdir+'stdcontrol.png', 0.4, 3.6, 0.4, '$\circ$C')

#********************************************************************************************************
# Signal: end of century Feedback response
members = clim_defs.clim_lat_lon('feedback',season,varcode)

ensmean, ensstd = ensemble_functions.stats(members) 
ensdiff = (ensmean - ensmean_control)#.mean(dim='member'))

plot_functions.plot_single_lat_lon(ensdiff, ensmean['lat'], ensmean['lon'], '(a) GEO8.5$_{2075-2095}$ - Base$_{2010-2030}$', outdir+varcode+'_clim_feedback-control_'+season+'.png', 3.6, 0.4, 3.6, 0.4, '$^{\circ}$C')

#********************************************************************************************************
# Signal-to-noise ratio 
SNR = abs(ensdiff)/stdcontrol
plot_functions.plot_ToE(SNR, ensmean['lat'], ensmean['lon'], '(c) SNR', outdir+'SNR.png', 0.2, 2.2, 0.2, '')

#********************************************************************************************************
