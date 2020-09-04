import glob
import matplotlib as mpl
mpl.use('Agg')
import surface_temp
import ensemble_functions
import plot_functions
import numpy as np
import xarray as xr

#********************************************************************************************************
season = 'DJF'
outdir="/Users/abanerjee/scripts/glens/output/"
var = "TREFHT"
alpha = 0.05

#********************************************************************************************************
# 1) ensemble mean raw field or end metric?
# 2) difference of averages or average of 400 differences?

#********************************************************************************************************
# control 
print("Calculating climatology for CONTROL")

members_control = []
for i in range(1,21):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0."+var+".201001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, tim1=2010, tim2=2030, var=var)
   ann_lon_lat = Ts_inst.annual_lon_lat(season)
   members_control.append(ann_lon_lat)
print("...done")

dim = 'member'
new_coord = range(len(members_control))

func = lambda *x: np.stack(x, axis=-1)
stack = xr.apply_ufunc(func, *members_control,
                     output_core_dims=[[dim]],
                     join='outer',
                     dataset_fill_value=np.nan)
stack[dim] = new_coord

ensmean = stack.mean('member')
ensstd = stack.std('member')

#ensmean_control, ensstd_control = ensemble_functions.stats(members_control) 

# internal variability
residuals = stack - ensmean
stdcontrol = residuals.std(dim=('time','member'))
plot_functions.plot_ToE(stdcontrol, 'Interannual $\sigma$', outdir+'stdcontrol.png', 0, 3.6, 0.4, '$\circ$C', projection='NorthPolarStereo')

# climatological mean
ensmean_control = ensmean.mean('time')

###
#members_control = []
#for i in range(1,21):
#   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
#   Ts_inst = surface_temp.Ts(ncpath, tim1=2020, tim2=2095, var=var)
#   ann_lon_lat = Ts_inst.annual_lon_lat(season)
#   members_control.append(ann_lon_lat)
#print("...done")
#
#dim = 'member'
#new_coord = range(len(members_control))
#
#func = lambda *x: np.stack(x, axis=-1)
#stack = xr.apply_ufunc(func, *members_control,
#                     output_core_dims=[[dim]],
#                     join='outer',
#                     dataset_fill_value=np.nan)
#stack[dim] = new_coord
#
#ensmean = stack.mean('member')
#ensstd = stack.std('member')
#
##ensmean_control, ensstd_control = ensemble_functions.stats(members_control) 
#
## internal variability
#residuals = stack - ensmean
#stdcontrol = residuals.std(dim=('time','member'))
##plot_functions.plot_ToE(stdcontrol, '', outdir+'stdcontrol.png', 0, 3.6, 0.4, 'degrees C', projection='NorthPolarStereo')
#********************************************************************************************************
# feedback runs
print("Calculating climatology for FEEDBACK")

members_feedback = []
for i in range(1,21):
   ncpath = glob.glob("/Volumes/CESM-GLENS/GLENS/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+"/atm/proc/tseries/month_1/Combined/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0."+var+".202001-*.nc")[0]
   Ts_inst = surface_temp.Ts(ncpath, tim1=2075, tim2=2095, var=var)
   clim_lon_lat = Ts_inst.climatology_lon_lat(season)
   members_feedback.append(clim_lon_lat)

ensmean_feedback, ensstd_feedback = ensemble_functions.stats(members_feedback) 
ensdiff_feedback = ensmean_feedback - ensmean_control
plot_functions.plot_single_lat_lon(ensdiff_feedback, ensdiff_feedback['lat'], ensdiff_feedback['lon'], 'Feedback (2075-2095) -\nBase (2010-2030)', outdir+'Ts_ensdiff_feedback-control_'+season+'.png', 3.6, 0.4, 3.6, 0.4, '$^{\circ}$C')

#********************************************************************************************************
# SNR
SNR = abs(ensdiff_feedback)/stdcontrol
#plot_functions.plot_ToE(SNR, 'SNR', outdir+'SNR.png', 0, 2.2, 0.2, '', projection='NorthPolarStereo')

#********************************************************************************************************
