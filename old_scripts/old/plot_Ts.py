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
import surface_temp

#********************************************************************************************************
season = 'DJF'
outdir="/home/ab4283/scripts/glens/output/"

#********************************************************************************************************
# Plot
def plot_anomaly(z, title, outname, lon, lat, colorbar=True):

   fig = plt.figure(figsize=(9, 6.5))

   # some plot parameters
   llim = -6
   ulim = 6
   lby = 1 
   tby = 1 
   levs = np.arange(llim,ulim+lby,lby)
   cticks = np.arange(llim,ulim+tby,tby)

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
   llat = -90 
   ulat = 90
   llon = -180
   ulon = 180

   map = Basemap(projection='cyl',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon, fix_aspect=False)
   # cylindrical is regular in latitude/longitude so no complicated mapping onto map coordinates
   x, y = map(glon,glat)

   cols     = ccol.custom_colors('grads')

   plt_ax = fig.add_axes([0.12, 0.27, 0.83, 0.65]) # left, bottom, width, height
   cplot=map.contourf(x,y,ibase,levs,extend="both", cmap=cols, ax=plt_ax)
   # plot coastlines, draw label meridians and parallels.
   map.drawcoastlines(linewidth=1,color="black")
   #map.drawcountries(linewidth=0.5,color="black")
   #map.drawstates()
   map.drawparallels(np.arange(-90,100,30),labels=[1,0,0,0],fontsize=26,linewidth=0)
   map.drawmeridians(np.arange(-180,240,60),labels=[0,0,0,1],fontsize=26,linewidth=0)
   map.drawmapboundary()
   plt.title(title, fontsize=30, weight='bold')
   #plt.figtext(0.12,0.93,plotlett, size=30, weight='bold')

   ##print 'ok4'
   #if zsig!=0:
   #   # Shade OUT non-significance
   #   itvals,itlon = addcyclic(zsig['tvals'],lon)
   #   for m in range(len(itlon)-1):
   #      for n in range(len(lat)-1):
   #         print m, len(itlon)-1
   #         if(itvals[n,m]<zsig['pval']):
   #            x1 = itlon[m]
   #            x2 = itlon[m+1]
   #            y1 = lat[n]
   #            y2 = lat[n+1]
   #            plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='//',linewidth=0)
   #            plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='\\',linewidth=0)

   if colorbar:
      cbar_ax = fig.add_axes([0.12, 0.13, 0.83, 0.04])
      cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=cticks)
      cbar.set_label('$^{\circ}$C',size=26)#,labelpad=-0.09)
      cbar.ax.tick_params(labelsize=24)
   plt.savefig(outdir+outname+'.png')
   plt.close()

#********************************************************************************************************
# Plot
def plot_ensemble_anomaly(members,lon,lat):

   def plot_single_member(z, inens, count):
      print z.shape
      col = mod(count,5)+1
      row = (count/5)+1
   
      # some plot parameters
      llim = 6
      lby = 1
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
      llat = -90
      ulat = 90
      llon = -180
      ulon = 180

      map = Basemap(projection='cyl',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon, fix_aspect=False)
      # cylindrical is regular in latitude/longitude so no complicated mapping onto map coordinates
      x, y = map(glon,glat)

      cols     = ccol.custom_colors('grads')

      ax = plt.subplot2grid((4,5), (row-1,col-1))#, colspan=1)
      cplot=map.contourf(x,y,ibase,levs,extend="both", cmap=cols)
      # plot coastlines, draw label meridians and parallels.
      map.drawcoastlines(linewidth=1,color="black")
      map.drawmapboundary()
      plt.title(str(inens),x=0.08,y=1.02)
    
      return (cplot, cticks)

   pp = PdfPages(outdir+'members.pdf')
   fig = plt.figure(figsize=(11, 8))#, dpi=100)
   count = 0
   for inens in range(len(diffs)):
      cplot, cticks = plot_single_member(diffs[inens], inens+1, count) 
      count+=1
   plt.suptitle('Feedback - Control, members', fontsize=30, weight="bold")
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

#********************************************************************************************************
paths_feedback = []
for i in range(1,21): 
   ncpath = "/dx03/ab4283/GLENS/feedback/b.e15.B5505C5WCCML45BGCR.f09_g16.feedback.0"+str(i).zfill(2)+".cam.h0.TREFHT.202001-209912.nc"
   print ncpath
   paths_feedback.append(ncpath)

c1 = "/dx03/ab4283/GLENS/control/b.e15.B5505C5WCCML45BGCR.f09_g16.control.001.cam.h0.TREFHT.201001-209906.nc"
c2 = "/dx03/ab4283/GLENS/control/b.e15.B5505C5WCCML45BGCR.f09_g16.control.002.cam.h0.TREFHT.201001-209807.nc"
c3 = "/dx03/ab4283/GLENS/control/b.e15.B5505C5WCCML45BGCR.f09_g16.control.003.cam.h0.TREFHT.201001-209912.nc"
paths_control = [c1,c2,c3]
for i in range(4,21):
   ncpath = "/dx03/ab4283/GLENS/control/b.e15.B5505C5WCCML45BGCR.f09_g16.control.0"+str(i).zfill(2)+".cam.h0.TREFHT.201001-203012.nc"
   paths_control.append(ncpath)
paths_control = [c1]

surfTs_feedback = []
for run in paths_feedback:
    lon, lat, surfT = surface_temp.surf_T(run, 2020, 2075, 2094, time_mean=season, xlonname='lon', xlatname='lat', xtimname='time', varname='TREFHT', lonstart=0)
    surfTs_feedback.append(surfT)

surfTs_control = []
for run in paths_control:
    lon, lat, surfT = surface_temp.surf_T(run, 2010, 2011, 2030, time_mean=season, xlonname='lon', xlatname='lat', xtimname='time', varname='TREFHT', lonstart=0)
    surfTs_control.append(surfT)

# plot control
print np.array(surfTs_control).shape
mean_surfTs_control = np.mean(np.array(surfTs_control), axis=0)
plot_anomaly(mean_surfTs_control, 'control', 'Control', lon, lat)

# plot ensemble mean difference
mean_surfTs_feedback = np.mean(np.array(surfTs_feedback), axis=0)
ensdiff = mean_surfTs_feedback - mean_surfTs_control
plot_anomaly(ensdiff, 'Feedback-Control ensemble mean', 'ensdiff', lon, lat)

# plot members differences
diffs = []
for run in surfTs_feedback:
   diff = run - mean_surfTs_control
   diffs.append(diff)
plot_ensemble_anomaly(diffs, lon, lat)

   
