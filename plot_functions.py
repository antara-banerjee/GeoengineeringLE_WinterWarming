'''
Plotting functions.
Includes latitude-height and latitude-longitude cross sections.
'''

#********************************************************************************************************
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.path as mpath
import matplotlib as mpl
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
import custom_colors as ccol

#********************************************************************************************************
# LATITUDE-HEIGHT CROSS SECTIONS
#********************************************************************************************************
# One plot, latitude-height cross section
def plot_single_lat_hgt(z, zbase, title, outname, lim, by, cbarlim, cbarby, clim, cby, cdp, clabel, zsig=0, colorbar=True):

   fig = plt.figure(figsize=(4.5, 3.5), dpi=300)

   # some plot parameters
   levs = np.arange(-lim,lim+by,by)
   clevs = np.arange(-clim,clim+cby,cby)
   cbarticks = np.arange(-cbarlim,cbarlim+cbarby,cbarby)
   bottom = 1000
   top = 1
   xlab = 'Latitude'
   ylab = 'Pressure (hPa)'
   cols = ccol.custom_colors('BlueRed')

   # main plot
   fig.add_axes([0.12, 0.15, 0.65, 0.75]) # left, bottom, width, height
   cplot=plt.contourf(z.lat, -np.log10(z.level), z, levs, extend="both", cmap=cols)
   cplot2=plt.contour(zbase.lat, -np.log10(zbase.level), zbase, clevs, colors='black', hold='on', linewidths=0.5)
   plt.clabel(cplot2, fontsize=6, fmt='%.'+str(cdp)+'f') 
   plt.title(title, fontsize=12)
   plt.xlabel(xlab,fontsize=10)
   plt.ylabel(ylab,fontsize=10, labelpad=-5)
   plt.xticks(np.arange(-90,120,30), [r'90$^{\circ}$S',r'60$^{\circ}$S',r'30$^{\circ}$S',r'0$^{\circ}$',r'30$^{\circ}$N',r'60$^{\circ}$N',r'90$^{\circ}$N'])
   yticks = [1000,100,10,1,0.1]
   plt.yticks(-np.log10(yticks),yticks)
   plt.ylim((-np.log10(bottom),-np.log10(top)))
   plt.tick_params(axis='both', which='major', labelsize=10)

   # shade OUT non-significance 
   if type(zsig) is int: # default, no significance shown
      zsig = np.zeros([len(zlat),len(zlon)])
   mpl.rcParams['hatch.linewidth'] = 0.1
   plt.contourf(z.lat, -np.log10(z.level), zsig, levels=[-1,0,1], hatches=[None,'...'], colors='none')

   # colorbar
   if colorbar:
      cbar_ax = fig.add_axes([0.83, 0.15, 0.04, 0.75])
      cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='vertical', ticks=cbarticks)
      cbar.set_label(clabel,size=10)
      cbar.ax.tick_params(labelsize=10)

   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
# Multi-plot, latitude-height cross section
def plot_matrix_lat_hgt(members, zbase, lat, hgt, title, outname, lim, by, cbarlim, cbarby, clim, cby, clabel):

   # some plot parameters
   levs = np.arange(-lim,lim+by,by)
   clevs = np.arange(-clim,clim+cby,cby)
   cbarticks = np.arange(-cbarlim,cbarlim+cbarby,cbarby)
   bottom = 1000
   top = 1
   cols = ccol.custom_colors('BlueRed')

   def plot_single_member(z, inens, count):
      col = int((count%5))+1
      row = int((count/5))+1
   
      ax = plt.subplot2grid((4,5), (row-1,col-1))
      cplot=ax.contourf(lat, -np.log10(hgt), z, levs, extend="both", cmap=cols)
      cplot2=ax.contour(lat, -np.log10(hgt), zbase, clevs, colors='black', hold='on', linewidths=0.5)
      ax.set_title(str(inens),x=0.08,y=1.02)
      ax.set_ylim([-np.log10(bottom), -np.log10(top)])
      yticks = [bottom,100,10,1]

      # declutter labels and tickmarks
      if (col==1 and row==4):
         ax.set_yticks(-np.log10(yticks),yticks)
         ax.set_yticklabels(yticks)
         ax.set_xticks(np.arange(-90,120,30))
         ax.set_xticklabels(['-90$^{\circ}$','','',r'0$^{\circ}$',r'',r'',r'90$^{\circ}$'])
      elif col==1:
         ax.set_yticks(-np.log10(yticks),yticks)
         ax.set_yticklabels(yticks)
         ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
      elif row==4:
         ax.set_xticks(np.arange(-90,120,30))
         ax.set_xticklabels(['-90$^{\circ}$','','',r'0$^{\circ}$',r'',r'',r'90$^{\circ}$'])
         ax.tick_params(axis='y',which='both',left=False,right=False,labelleft=False)
      else:
         ax.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False)
    
      return cplot

   fig = plt.figure(figsize=(11, 8))

   # subplots
   count = 0
   for inens in range(len(members)):
      cplot = plot_single_member(members[inens], inens+1, count) 
      count+=1

   # global features
   plt.suptitle(title, fontsize=24, weight="bold")
   fig.subplots_adjust(bottom=0.05, top=0.90, left=0.05, right=0.89)
   cax = fig.add_axes([0.91, 0.05, 0.02, 0.85]) # left, bottom, width, height
   cbar=plt.colorbar(cplot, cax=cax, orientation='vertical', ticks=cbarticks)
   cbar.set_label(clabel, size=16)
   cbar.ax.tick_params(labelsize=16)
   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
# LATITUDE-LONGITUDE CROSS SECTIONS
#********************************************************************************************************
# One plot, latitude-longitude map 
def plot_single_lat_lon(z, zlat, zlon, title, outname, lim, by, cbarlim, cbarby, clabel, zsig=0, colorscale='BlueRed'):
    
   fig = plt.figure(figsize=(6, 6), dpi=300)

   # some plot parameters
   levs = np.arange(-lim,lim+by,by)
   cbarticks = np.arange(-cbarlim,cbarlim+cbarby,cbarby)
   cols = ccol.custom_colors(colorscale)
   
   # set up map
   prj = ccrs.NorthPolarStereo()
   ax = fig.add_axes([0.05, 0.05, 0.9, 0.90], projection=prj) # left, bottom, width, height
   ax.coastlines()
   
   # has to be done before data to plot added for use_as_clip_path to work
   llon=-180
   ulon=180
   llat=20
   ulat=90
   ax.set_extent([llon, ulon, llat, ulat], ccrs.PlateCarree())
   theta = np.linspace(0, 2*np.pi, 100)
   center, radius = [0.5, 0.5], 0.5
   verts = np.vstack([np.sin(theta), np.cos(theta)]).T
   circle = mpath.Path(verts * radius + center)
   ax.set_boundary(circle, transform=ax.transAxes, use_as_clip_path=True)

   # add data
   # add cyclic point to wrap around in longitude (cartopy function); outputs as np array
   # if using pyplot: ibase,ilon = user_addcyclic(z,np.array(lon))     
   cyclic_z, cyclic_lon = add_cyclic_point(z, coord=zlon)
   cplot = ax.contourf(cyclic_lon, zlat, cyclic_z, transform=ccrs.PlateCarree(), extend='both', levels=levs, cmap=cols)
   plt.title(title, fontsize=18)

   # shade OUT non-significance
   if type(zsig) is int: # default, no significance shown
      zsig = np.zeros([len(zlat),len(zlon)])
   cyclic_zsig, cyclic_tlon = add_cyclic_point(zsig, coord=zlon)
   cplot_t = ax.contourf(cyclic_lon, zlat, cyclic_zsig, transform=ccrs.PlateCarree(),levels=[-1,0,1],hatches=[None,'..'],colors='none')

   # colorbar
   cbar=plt.colorbar(cplot, orientation='vertical', ticks=cbarticks)
   cbar.set_label(clabel, size=14)
   cbar.ax.tick_params(labelsize=14)
   
   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
def plot_matrix_lat_lon(members, zlat, zlon, title, outname, lim, by, cbarlim, cbarby, clabel, colorscale='BlueRed'):

   # some plot parameters
   levs = np.arange(-lim,lim+by,by)
   cbarticks = np.arange(-cbarlim,cbarlim+cbarby,cbarby)
   cols     = ccol.custom_colors(colorscale)

   def plot_single_member(z, inens, count):
      col = int(count%5)+1
      row = int((count/5))+1
   
      # set up map
      prj = ccrs.NorthPolarStereo()
      ax = plt.subplot2grid((4,5), (row-1,col-1), projection=prj)
      ax.coastlines()

      # has to be done before data to plot added for use_as_clip_path to work
      llon=-180
      ulon=180
      llat=20
      ulat=90
      ax.set_extent([llon, ulon, llat, ulat], ccrs.PlateCarree())
      theta = np.linspace(0, 2*np.pi, 100)
      center, radius = [0.5, 0.5], 0.5
      verts = np.vstack([np.sin(theta), np.cos(theta)]).T
      circle = mpath.Path(verts * radius + center)
      ax.set_boundary(circle, transform=ax.transAxes, use_as_clip_path=True)

      cyclic_z, cyclic_lon = add_cyclic_point(z, coord=zlon)
      cplot = ax.contourf(cyclic_lon, zlat, cyclic_z, transform=ccrs.PlateCarree(), extend='both', levels=levs, cmap=cols)

      ax.set_title(str(inens),x=0.08,y=1.02)
    
      return cplot

   fig = plt.figure(figsize=(11, 8))

   # subplots
   count = 0
   for inens in range(len(members)):
      cplot = plot_single_member(members[inens], inens+1, count) 
      count+=1

   # global features
   plt.suptitle(title, fontsize=24, weight="bold")
   fig.subplots_adjust(bottom=0.05, top=0.95, left=0.02, right=0.86)
   cax = fig.add_axes([0.88, 0.05, 0.02, 0.90]) # left, bottom, width, height
   cbar=plt.colorbar(cplot, cax=cax, orientation='vertical', ticks=cbarticks)
   cbar.set_label(clabel, size=16)
   cbar.ax.tick_params(labelsize=16)
   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
# Time of emergence figure 
def plot_ToE(z, zlat, zlon, title, outname, llim, ulim, by, clabel):
    
   fig = plt.figure(figsize=(6, 6), dpi=300)

   # some plot parameters
   levs = np.arange(llim,ulim+by,by)
   cticks = np.arange(llim,ulim+by,by)
   
   # set up map
   prj = ccrs.NorthPolarStereo()
   ax = fig.add_axes([0.05, 0.05, 0.9, 0.90], projection=prj) # left, bottom, width, height
   ax.coastlines()
   
   # has to be done before data to plot added for use_as_clip_path to work
   llon=-180
   ulon=180
   llat=20
   ulat=90
   ax.set_extent([llon, ulon, llat, ulat], ccrs.PlateCarree())
   theta = np.linspace(0, 2*np.pi, 100)
   center, radius = [0.5, 0.5], 0.5
   verts = np.vstack([np.sin(theta), np.cos(theta)]).T
   circle = mpath.Path(verts * radius + center)
   ax.set_boundary(circle, transform=ax.transAxes, use_as_clip_path=True)

   # add data
   # add cyclic point to wrap around in longitude (cartopy function); outputs as np array
   #cyclic_z, cyclic_lon = add_cyclic_point(z, coord=z['lon'])
   cyclic_z, cyclic_lon = add_cyclic_point(z, coord=zlon)
   cplot = ax.contourf(cyclic_lon, zlat, cyclic_z, transform=ccrs.PlateCarree(), extend='both', levels=levs, cmap=cm.afmhot)
   plt.title(title, fontsize=18)

   # colorbar
   cbar=plt.colorbar(cplot, orientation='vertical', ticks=cticks)
   cbar.set_label(clabel,size=12)
   cbar.ax.tick_params(labelsize=12)
   
   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
# END
#********************************************************************************************************
