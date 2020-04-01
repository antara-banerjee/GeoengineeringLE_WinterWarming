import numpy as np
import scipy.stats as ss
import netCDF4 as ncdf
import matplotlib as mpl
import matplotlib.pyplot as plt
#plt.ioff()
import calendar
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
from matplotlib.backends.backend_pdf import PdfPages
# mpl_toolkits contain the class Basemap and other functions such
# as addcyclic, shiftgrid etc.
from pylab import *
import matplotlib.cm as cm
import matplotlib.colors as colors
import custom_colors as ccol
import numpy.ma as ma
import get_netcdf_attributes as ncdf_att

def surf_T(ncpath, time0, tim1, tim2, time_mean, xlonname='lon', xlatname='lat', xtimname='time', varname='', lonstart=0):

   # load netcdf file
   ncmod     = ncdf_att.get_ncmod(ncpath)

   # get raw field
   var, = ncdf_att.get_vars(ncmod, varname)

   # dimensions
   lon, lat, tim = ncdf_att.get_dims(ncmod, lonname=xlonname, latname=xlatname, timname=xtimname)

   # shuffle in longitude if needed
   oldlon = np.copy(lon)
   if lonstart==0:
      lon = oldlon - 180
      rollby = np.where(oldlon==180)[0][0]
      var = np.roll(var, -rollby, axis=2)

   #**************************************************
   def time_subset(invar):

      itim1 = (tim1 - time0)*12
      itim2 = (tim2 - time0)*12+12+2
      var_tsub = invar[itim1:itim2,:,:]
      tsub = var_tsub.shape[0]
      nsubyrs = tsub/12

      return (var_tsub, nsubyrs)
   
   #**************************************************
   def seasonal_mean(invar, invar_nyrs, time_mean):

       if time_mean=='monthly':
          v_tmean = invar
       elif time_mean=='clim_monthly':
          v_tmean = np.empty(12)
          for i in range(12):
             j = np.arange(i, invar_nyrs*12, 12)
             v_tmean[i] = np.mean(invar[j], axis=0, dtype=np.float64)
       else:
          v_tmean = np.empty([invar_nyrs])
          if time_mean=='annual':
             for i in range(invar_nyrs):
                jan = 12*i
                v_tmean[i] = np.mean(invar[jan:jan+12], axis=0, dtype=np.float64)
          else:
             startmon_dict = {'JJA':5,'DJF':11,'MAM':2,'SON':8,'NDJF':10,'D':11,'J':0,'F':1}
             len_season = len(time_mean)
             v_tmean = np.zeros([invar_nyrs, len(lat), len(lon)])
             for i in range(invar_nyrs):
                startmon = 12*i+startmon_dict[time_mean]
                v_tmean[i,:,:] = np.mean(invar[startmon:startmon+len_season,:,:], axis=0, dtype=np.float64)

       return v_tmean

   #**************************************************
   # seasonal mean then average over climatological time period
   var_tsub, nsubyrs = time_subset(var)
   var_seas = seasonal_mean(var_tsub, nsubyrs, time_mean)
   var_tave = np.mean(var_seas, axis=0)
   
   return (lon, lat, var_tave)

#********************************************************************************************************
def calc_ensemble_mean(mods_all, nens):

   ensmean = np.mean(mods_all, axis=2)
   # one sample t-test; t statistic = (mean-0)/std*sqrt(N) or N-1?
   ensstd = np.std(mods_all, axis=2, ddof=1)
   tvals = abs(ensmean)/ensstd*np.sqrt(nens-1)#; print tvals.shape

   return (ensmean, ensstd, tvals)

#********************************************************************************************************
# Plot
def plot_anomaly(z, title, outname, lon, lat, plotlett, volname, colorbar=False, zsig=0):

   fig = plt.figure(figsize=(9, 6.5))

   # some plot parameters
   llim =  6
   lby = 0.5
   tby = 1 
   levs = np.arange(-llim,llim+lby,lby)
   cticks = np.arange(-llim,llim+tby,tby)

   # make cyclic for plotting (add the first longitude + its data to the end)
   ibase,ilon = addcyclic(z,lon)
   icbase,iclon = addcyclic(z,lon)

   # set up grid for plotting
   glon, glat = np.meshgrid(ilon, lat)

   cmap = cm.bwr
   cnorm=colors.Normalize(cmap,clip=False)
   cmap.set_under(color=cmap(0.0),alpha=1.0)
   cmap.set_over(color=cmap(1.0),alpha=1.0)

   # lat/lon boundaries for regions
   llat = 0
   ulat = 90
   llon = -180
   ulon = 180
   #llat = -90
   #ulat = 90
   #llon = -180
   #ulon = 180

   map = Basemap(projection='cyl',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon, fix_aspect=False)
   # cylindrical is regular in latitude/longitude so no complicated mapping onto map coordinates
   x, y = map(glon,glat)

   cols     = ccol.custom_colors('grads')

   plt_ax = fig.add_axes([0.12, 0.27, 0.83, 0.65]) # left, bottom, width, height
   print 'ok1'
   cplot=map.contourf(x,y,ibase,levs,extend="both", cmap=cols, ax=plt_ax)
   print 'ok2'
   # plot coastlines, draw label meridians and parallels.
   map.drawcoastlines(linewidth=1,color="black")
   #map.drawcountries(linewidth=0.5,color="black")
   #map.drawstates()
   map.drawparallels(np.arange(-90,100,30),labels=[1,0,0,0],fontsize=26,linewidth=0)
   map.drawmeridians(np.arange(-180,240,60),labels=[0,0,0,1],fontsize=26,linewidth=0)
   print 'ok3'
   map.drawmapboundary()
   plt.title(plotlett+" "+title, fontsize=30, weight='bold')
   #plt.figtext(0.12,0.93,plotlett, size=30, weight='bold')

   #print 'ok4'
   if zsig!=0:
      # Shade OUT non-significance
      itvals,itlon = addcyclic(zsig['tvals'],lon)
      for m in range(len(itlon)-1):
         for n in range(len(lat)-1):
            print m, len(itlon)-1
            if(itvals[n,m]<zsig['pval']):
               x1 = itlon[m]
               x2 = itlon[m+1]
               y1 = lat[n]
               y2 = lat[n+1]
               plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='//',linewidth=0)
               plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='\\',linewidth=0)

   print 'ok5'
   if colorbar:
      cbar_ax = fig.add_axes([0.12, 0.13, 0.83, 0.04])
      cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=cticks)
      cbar.set_label('$^{\circ}$C',size=26)#,labelpad=-0.09)
      cbar.ax.tick_params(labelsize=24)
   plt.savefig(outdir+'volcano_'+outname+'_surface_temp_'+volname+'.png')
   plt.close()

#********************************************************************************************************
# Plot
def plot_ensemble_anomaly(mods_all,modname,ens1,ens2,lon,lat):

   def plot_single_member(z, inens, count):
      print z.shape
      col = mod(count,5)+1
      row = (count/5)+1
   
      # some plot parameters
      llim =  6
      lby = 0.5
      tby = 1
      levs = np.arange(-llim,llim+lby,lby)
      cticks = np.arange(-llim,llim+tby,tby)

      # make cyclic for plotting (add the first longitude + its data to the end)
      ibase,ilon = addcyclic(z,lon)
      icbase,iclon = addcyclic(z,lon)

      # set up grid for plotting
      glon, glat = np.meshgrid(ilon, lat)

      cmap = cm.bwr
      cnorm=colors.Normalize(cmap,clip=False)
      cmap.set_under(color=cmap(0.0),alpha=1.0)
      cmap.set_over(color=cmap(1.0),alpha=1.0)

      # lat/lon boundaries for regions
      llat = 0
      ulat = 90
      llon = -180
      ulon = 180

      map = Basemap(projection='cyl',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon, fix_aspect=False)
      # cylindrical is regular in latitude/longitude so no complicated mapping onto map coordinates
      x, y = map(glon,glat)

      cols     = ccol.custom_colors('grads')

      ax = plt.subplot2grid((5,5), (row-1,col-1))#, colspan=1)
      cplot=map.contourf(x,y,ibase,levs,extend="both", cmap=cols)
      # plot coastlines, draw label meridians and parallels.
      map.drawcoastlines(linewidth=1,color="black")
      map.drawmapboundary()
      plt.title(str(inens),x=0.08,y=1.02)
    
      return (cplot, cticks)

   pp = PdfPages(outdir+'volcano_'+modname+'_members_'+str(ens1)+'-'+str(ens2)+'_surface_temp.pdf')
   fig = plt.figure(figsize=(11, 8))#, dpi=100)
   count = 0
   for inens in range(ens1,ens2+1):
      cplot, cticks = plot_single_member(mods_all[:,:,inens-1], inens, count) 
      count+=1
   plt.suptitle(modname, fontsize=30, weight="bold")
   plt.tight_layout()
   #left, bottom, width, height
   fig.subplots_adjust(bottom=0.15, top=0.90, left = 0.05, right=0.95)
   cbar_ax = fig.add_axes([0.03, 0.10, 0.94, 0.03])
   cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=cticks)
   #cbar.set_label("$T_s$$'$ / $^{\circ}$C",size=26,labelpad=-0.05)
   cbar.set_label("$^{\circ}$C",size=26,labelpad=-0.05)
   cbar.ax.tick_params(labelsize=24)
   pp.savefig(fig)
   pp.close()

   
