'''
Signal-to-noise ratio testing in geoengineering runs.
Signal is defined as ensemble mean end-of-century geoengineering response relative to Base.
Noise is defined as interannual standard deviation of Base runs.
The signal, noise and S/N ratio are all shown for near-surface air temperature in publication. 
'''

# standard imports
import glob
import numpy as np
import xarray as xr

# user imports
import clim_defs 
import ensemble_defs
import plot_defs
import vartimeproc

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
varcode = 'TREFHT'

#********************************************************************************************************
# 1) Plot interannual sigma from Base variability
# annual, seasonal mean
members_control = []
for i in range(1,21):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+varcode+".201001-*.nc")[0]
   vartimeobj = vartimeproc.VarTimeProc(ncpath, tim1=2010, tim2=2030, varcode=varcode)
   ann = vartimeobj.annual_mean(season)
   members_control.append(ann)

# adding coordinate 
dim = 'member'
new_coord = range(len(members_control))

func = lambda *x: np.stack(x, axis=-1)
stack = xr.apply_ufunc(func, *members_control,
                     output_core_dims=[[dim]],
                     join='outer',
                     dataset_fill_value=np.nan)
stack[dim] = new_coord

# Interannual sigma from residuals of annual means from member average gives similar results 
ensmean_control = stack.mean(dim=('time','member'))
ensstd_control = stack.std(dim=('time','member'))

plot_defs.plot_ToE(ensstd_control, ensstd_control['lat'], ensstd_control['lon'], '(b) Interannual $\sigma$', outdir+'stdcontrol.png', 0.4, 3.6, 0.4, '$\circ$C')

#********************************************************************************************************
# 2) Signal: end of century Feedback response
members = clim_defs.clim_lat_lon('feedback',season,varcode)

ensmean, ensstd = ensemble_defs.stats(members) 
ensdiff = ensmean - ensmean_control

plot_defs.plot_single_lat_lon(ensdiff, ensmean['lat'], ensmean['lon'], '(a) GEO8.5$_{2075-2095}$ - Base$_{2010-2030}$', outdir+varcode+'_clim_feedback-control_'+season+'.png', 3.6, 0.4, 3.6, 0.4, '$^{\circ}$C')

#********************************************************************************************************
# 3) Signal-to-noise ratio 
SNR = abs(ensdiff)/ensstd_control
plot_defs.plot_ToE(SNR, ensmean['lat'], ensmean['lon'], '(a) End-of-century\nSNR', outdir+'SNR.png', 0.2, 2.2, 0.2, '')

#********************************************************************************************************
