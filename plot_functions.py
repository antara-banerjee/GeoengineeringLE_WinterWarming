import numpy as np
import scipy.stats as ss
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
# mpl_toolkits contain the class Basemap and other functions such
# as addcyclic, shiftgrid etc.
import matplotlib.cm as cm
import custom_colors as ccol
#import get_netcdf_attributes as ncdf_att
from decimal import Decimal
from cartopy.util import add_cyclic_point
import cartopy.crs as ccrs
import matplotlib.path as mpath

#********************************************************************************************************
# PLOT FUNCTIONS
#********************************************************************************************************
# One plot, latitude-height cross section
def plot_single_lat_hgt(z, zbase, title, outname, flim, fby, clim, cby, clabel, zsig, colorbar=True):

   fig = plt.figure(figsize=(8, 8))

   # some plot parameters
   cdp = 0
   levs = np.arange(-flim,flim+fby,fby)
   clevs = np.arange(-clim,clim+cby,cby)
   #cbarticks = np.arange(-lim,lim+by,by)
   bottom = 1000
   top = 0.1
   ylabs    = [10**x for x in range(int(np.log10(bottom)),int(np.log10(10))-1,-1)]
   xlab     = 'Latitude'
   ylab     = 'Pressure (hPa)'

   cols     = ccol.custom_colors('grads')

   plt_ax = fig.add_axes([0.14, 0.25, 0.75, 0.65]) # left, bottom, width, height
   #plt_ax = fig.add_axes([0.12, 0.20, 0.83, 0.65]) # left, bottom, width, height
   cplot=plt.contourf(z.lat, -np.log10(z.level), z, levs, extend="both", cmap=cols)#, ax=plt_ax)
   cplot2=plt.contour(zbase.lat, -np.log10(zbase.level), zbase, clevs, colors='black', hold='on', linewidths=0.5)#, ax=plt_ax)
   plt.clabel(cplot2, fontsize=14, fmt='%.'+str(0)+'f') # add cdp into arguments
   plt.title(title, fontsize=24)
   #plt.xlabel(xlab,fontsize=26)
   plt.ylabel(ylab,fontsize=22,labelpad=-20)
   plt.tick_params(axis='both', which='major', labelsize=22)
   plt.xticks(np.arange(-90,120,30), ['90S','60S','30S',r'0$^{\circ}$',r'30$^{\circ}$N',r'60$^{\circ}$N',r'90$^{\circ}$N'])
   #plt.xticks(np.arange(-90,120,30))
   #yticks = [bottom,500,200,100,50,20,10,5]
   yticks = [bottom,100,10,1,0.1]
   plt.yticks(-np.log10(yticks),yticks)
   plt.ylim((-np.log10(bottom),-np.log10(top)))
   #plt.xlim([0,90])

   plt.contourf(z.lat, -np.log10(z.level), zsig, levels=[-1,0,1], hatches=[None,'.'], colors='none')

   ## Shade OUT non-significance
   #for m in range(len(lat)-1):
   #   for n in range(len(hgt)-1):
   #      print(m, len(lat))
   #      if zsig[n,m]:
   #         x1 = lat[m]
   #         x2 = lat[m+1]
   #         y1 = -np.log10(hgt[n])
   #         y2 = -np.log10(hgt[n+1])
   #         plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='//',linewidth=0)
   #         plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='\\',linewidth=0)

   if colorbar:
      #cbar_ax = fig.add_axes([0.17, 0.10, 0.77, 0.04])
      cbar_ax = fig.add_axes([0.14, 0.13, 0.75, 0.04])
      cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=np.arange(-5,6,1))
      cbar.set_label(clabel,size=22)#,labelpad=-0.09)
      cbar.ax.tick_params(labelsize=22)
   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
def plot_matrix_lat_hgt(members, zbase, lat, hgt, title, outname, flim, fby, clim, cby, clabel):

   cols     = ccol.custom_colors('grads')
   bottom = 1000
   top = 0.1

   def plot_single_member(z, inens, count):
      print(z.shape)
      col = mod(count,5)+1
      row = (count/5)+1
   
      # some plot parameters
      levs = np.arange(-flim,flim+fby,fby)
      clevs = np.arange(-clim,clim+cby,cby)

      ax = plt.subplot2grid((4,5), (row-1,col-1))#, colspan=1)
      cplot=contourf(lat, -np.log10(hgt), z, levs, extend="both", cmap=cols)#, ax=plt_ax)
      cplot2=contour(lat, -np.log10(hgt), zbase, clevs, colors='black', hold='on', linewidths=0.5)#, ax=plt_ax)
      #plt.clabel(cplot2, fontsize=16, fmt='%.'+str(0)+'f') # add cdp into arguments
      plt.title(str(inens),x=0.08,y=1.02)
      #plt.tick_params(axis='both', which='major', labelsize=22)
      #plt.xticks(np.arange(-90,120,30), ['90S','60S','30S',r'0$^{\circ}$',r'30$^{\circ}$N',r'60$^{\circ}$N',r'90$^{\circ}$N'])
      #plt.xticks(np.arange(-90,120,30))
      #yticks = [bottom,500,200,100,50,20,10,5]
      yticks = [bottom,100,10,1,0.1]
      #plt.yticks(-np.log10(yticks),yticks)
      plt.ylim((-np.log10(bottom),-np.log10(top)))
      plt.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False)
    
      return (cplot, levs)

   pp = PdfPages(outname)
   fig = plt.figure(figsize=(11, 8))#, dpi=100)
   count = 0
   for inens in range(len(members)):
      cplot, levs = plot_single_member(members[inens], inens+1, count) 
      count+=1
   plt.suptitle(title, fontsize=24, weight="bold")
   plt.tight_layout()
   #left, bottom, width, height
   fig.subplots_adjust(bottom=0.15, top=0.90, left = 0.05, right=0.95)
   cbar_ax = fig.add_axes([0.03, 0.10, 0.94, 0.03])
   cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=levs)
   #cbar.set_label("$T_s$$'$ / $^{\circ}$C",size=26,labelpad=-0.05)
   cbar.set_label(clabel,size=24,labelpad=-0.05)
   cbar.ax.tick_params(labelsize=24)
   pp.savefig(fig)
   pp.close()

#********************************************************************************************************
# One plot, latitude-longitude map 
def plot_single_lat_lon(z, title, outname, flim, fby, clim, cby, clabel, zsig=None, colorbar=True):
    
   fig = plt.figure(figsize=(6, 6))

   # some plot parameters
   levs = np.arange(-flim,flim+fby,fby)
   cticks = np.arange(-clim,clim+cby,cby)
   cols     = ccol.custom_colors('grads')
   
   # set up map
   prj = ccrs.NorthPolarStereo()
   #ax = fig.add_axes([0.10, 0.20, 0.8, 0.70], projection=prj) # left, bottom, width, height
   ax = fig.add_axes([0.05, 0.05, 0.9, 0.90], projection=prj) # left, bottom, width, height
   ax.coastlines()
   
   # set bound (such a pain in cartopy...)
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
   cyclic_z, cyclic_lon = add_cyclic_point(z, coord=z['lon'])
   #z.plot(transform=ccrs.PlateCarree(), levels=levs, cmap=cols)#, levels=levs)) # default xarray plot is plt.pcolormesh
   #z.plot.contourf(transform=ccrs.PlateCarree(), levels=levs, cmap=cols)#, levels=levs)) # does not work with cyclic_z which is not an xarray object
   cplot = ax.contourf(cyclic_lon, z.lat, cyclic_z, transform=ccrs.PlateCarree(), extend='both', levels=levs, cmap=cols)
   plt.title(title, fontsize=18)

   # Shade OUT non-significance
   cyclic_zsig, cyclic_tlon = add_cyclic_point(zsig, coord=z['lon'])
   cplot_t = ax.contourf(cyclic_lon, z.lat, cyclic_zsig, transform=ccrs.PlateCarree(),levels=[-1,0,1],hatches=[None,'.'],colors='none')

   # colorbar
   if colorbar:
      #cbar_ax = fig.add_axes([0.05, 0.13, 0.9, 0.04]) # left, bottom, width, height
      #cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=cticks)
      cbar=plt.colorbar(cplot, orientation='vertical', ticks=cticks)
      cbar.set_label(clabel,size=12)#,labelpad=-0.09)
      cbar.ax.tick_params(labelsize=12)
   
   plt.savefig(outname, dpi=300)
   plt.close()

#********************************************************************************************************
# One plot, height-month cross section
def plot_single_hgt_mon(z, zbase, hgt, title, outname, flim, fby, clim, cby, clabel, colorbar=True, zsig=0):

   #print z.shape
   #z = np.concatenate((z[5:12,:],z[0:5,:]), axis=0)
   #print z.shape
   #zbase = np.concatenate((zbase[5:12,:],zbase[0:5,:]), axis=0)

   #xlabels = ['J','J','A','S','O','N','D','J','F','M','A','M']
   xlabels = ['J','F','M','A','M','J','J','A','S','O','N','D']

   fig = plt.figure(figsize=(8, 8))

   # some plot parameters
   cdp = 0
   levs = np.arange(-flim,flim+fby,fby)
   clevs = np.arange(-clim,clim+cby,cby)
   #cbarticks = np.arange(-lim,lim+by,by)
   bottom = 1000
   top = 0.1
   ylabs    = [10**x for x in range(int(np.log10(bottom)),int(np.log10(10))-1,-1)]
   xlab     = 'Latitude'
   ylab     = 'Pressure (hPa)'

   cols     = ccol.custom_colors('grads')

   #plt_ax = fig.add_axes([0.18, 0.25, 0.75, 0.68]) # left, bottom, width, height
   plt_ax = fig.add_axes([0.12, 0.25, 0.83, 0.65]) # left, bottom, width, height
   #cplot=contourf(range(5,12)+range(0,5), -np.log10(hgt), np.transpose(z), levs, extend="both", cmap=cols)#, ax=plt_ax)
   #cplot2=contour(range(5,12)+range(0,5), -np.log10(hgt), np.transpose(zbase), clevs, colors='black', hold='on', linewidths=0.5)#, ax=plt_ax)
   cplot=contourf(range(0,12), -np.log10(hgt), np.transpose(z), levs, extend="both", cmap=cols)#, ax=plt_ax)
   cplot2=contour(range(0,12), -np.log10(hgt), np.transpose(zbase), clevs, colors='black', hold='on', linewidths=0.5)#, ax=plt_ax)
   #   plt.clabel(cplot2, fontsize=16, fmt='%.'+str(cdp)+'f')
   plt.title(title, fontsize=20, weight='bold')
   #plt.xlabel(xlab,fontsize=26)
   plt.ylabel(ylab,fontsize=22,labelpad=-20)
   plt.tick_params(axis='both', which='major', labelsize=22)
   #plt.xticks(np.arange(-90,120,30), ['90S','60S','30S',r'0$^{\circ}$',r'30$^{\circ}$N',r'60$^{\circ}$N',r'90$^{\circ}$N'])
   #plt.xticks(np.arange(-90,120,30))
   plt.xticks(range(12), xlabels)
   #yticks = [bottom,500,200,100,50,20,10,5]
   yticks = [bottom,100,10,1]
   plt.yticks(-np.log10(yticks),yticks)
   plt.ylim((-np.log10(bottom),-np.log10(top)))
   #plt.xlim([0,90])

   # Shade OUT non-significance
   for m in range(11):
      for n in range(len(hgt)-1):
         if zsig[m,n]:
            x1 = m
            x2 = m+1
            y1 = -np.log10(hgt[n])
            y2 = -np.log10(hgt[n+1])
            plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='//',linewidth=0)
            plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='\\',linewidth=0)

   if colorbar:
      #cbar_ax = fig.add_axes([0.17, 0.10, 0.77, 0.04])
      cbar_ax = fig.add_axes([0.12, 0.13, 0.83, 0.04])
      cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=levs)
      cbar.set_label(clabel,size=22)#,labelpad=-0.09)
      cbar.ax.tick_params(labelsize=22)
   plt.savefig(outname)
   plt.close()

#********************************************************************************************************
def plot_matrix_hgt_mon(members, zbase, hgt, title, outname, flim, fby, clim, cby, clabel):

   cols     = ccol.custom_colors('grads')
   bottom = 1000
   top = 0.1

   def plot_single_member(z, inens, count):
      print(z.shape)
      col = mod(count,5)+1
      row = (count/5)+1
   
      # some plot parameters
      levs = np.arange(-flim,flim+fby,fby)
      clevs = np.arange(-clim,clim+cby,cby)

      ax = plt.subplot2grid((4,5), (row-1,col-1))#, colspan=1)
      cplot=contourf(range(12), -np.log10(hgt), np.transpose(z), levs, extend="both", cmap=cols)#, ax=plt_ax)
      cplot2=contour(range(12), -np.log10(hgt), np.transpose(zbase), clevs, colors='black', hold='on', linewidths=0.5)#, ax=plt_ax)
      #plt.clabel(cplot2, fontsize=16, fmt='%.'+str(0)+'f') # add cdp into arguments
      plt.title(str(inens),x=0.08,y=1.02)
      #plt.tick_params(axis='both', which='major', labelsize=22)
      #plt.xticks(np.arange(-90,120,30), ['90S','60S','30S',r'0$^{\circ}$',r'30$^{\circ}$N',r'60$^{\circ}$N',r'90$^{\circ}$N'])
      #plt.xticks(np.arange(-90,120,30))
      #yticks = [bottom,500,200,100,50,20,10,5]
      yticks = [bottom,100,10,1,0.1]
      #plt.yticks(-np.log10(yticks),yticks)
      plt.ylim((-np.log10(bottom),-np.log10(top)))
      plt.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False)
    
      return (cplot, levs)

   pp = PdfPages(outname)
   fig = plt.figure(figsize=(11, 8))#, dpi=100)
   count = 0
   for inens in range(len(members)):
      cplot, levs = plot_single_member(members[inens], inens+1, count) 
      count+=1
   plt.suptitle(title, fontsize=24, weight="bold")
   plt.tight_layout()
   #left, bottom, width, height
   fig.subplots_adjust(bottom=0.15, top=0.90, left = 0.05, right=0.95)
   cbar_ax = fig.add_axes([0.03, 0.10, 0.94, 0.03])
   cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=levs)
   #cbar.set_label("$T_s$$'$ / $^{\circ}$C",size=26,labelpad=-0.05)
   cbar.set_label(clabel,size=24,labelpad=-0.05)
   cbar.ax.tick_params(labelsize=24)
   pp.savefig(fig)
   pp.close()

#********************************************************************************************************
def plot_matrix_lat_lon(members, lat, lon, title, outname, flim, fby, clabel):

   cols     = ccol.custom_colors('grads')

   def plot_single_member(z, inens, count):
      print(z.shape)
      col = int(mod(count,5))+1
      row = int((count/5))+1
   
      # some plot parameters
      levs = np.arange(-flim,flim+fby,fby)
      cticks = np.arange(-flim,flim+fby,fby)

      # make cyclic for plotting (add the first longitude + its data to the end)
      ibase,ilon = user_addcyclic(z,lon)
      icbase,iclon = user_addcyclic(z,lon)

      # set up grid for plotting
      glon, glat = np.meshgrid(ilon, lat)

      cmap = cm.bwr
      #cnorm=colors.Normalize(cmap,clip=False)
      cmap.set_under(color=cmap(0.0),alpha=1.0)
      cmap.set_over(color=cmap(1.0),alpha=1.0)

      print(row, col)
      ax = plt.subplot2grid((4,5), (row-1,col-1))#, colspan=1)
      m = Basemap(projection='npstere',boundinglat=20,lon_0=0,resolution='l',round=True)
      x, y = m(glon,glat)
      cplot=m.contourf(x,y,ibase,levs,extend="both", cmap=cols)
      m.drawcoastlines(linewidth=0.5)
      #m.fillcontinents(color='coral',lake_color='aqua')
      # draw parallels and meridians.
      #m.drawparallels(np.arange(-80.,81.,20.))
      #m.drawmeridians(np.arange(-180.,181.,20.))
      m.drawmapboundary()
      plt.title(str(inens),x=0.08,y=1.02)

      ## lat/lon boundaries for regions
      #llat = -90
      #ulat = 90
      #llon = -180
      #ulon = 180

      #map = Basemap(projection='cyl',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon, fix_aspect=False)
      ## cylindrical is regular in latitude/longitude so no complicated mapping onto map coordinates
      #x, y = map(glon,glat)

      #cols     = ccol.custom_colors('grads')

      #ax = plt.subplot2grid((4,5), (row-1,col-1))#, colspan=1)
      #cplot=map.contourf(x,y,ibase,levs,extend="both", cmap=cols)
      ## plot coastlines, draw label meridians and parallels.
      #map.drawcoastlines(linewidth=1,color="black")
      #map.drawmapboundary()
      #plt.title(str(inens),x=0.08,y=1.02)
    
      return (cplot, cticks)

   pp = PdfPages(outname)
   fig = plt.figure(figsize=(11, 8))#, dpi=100)
   count = 0
   for inens in range(len(members)):
      cplot, cticks = plot_single_member(members[inens], inens+1, count) 
      count+=1
   plt.suptitle(title, fontsize=24, weight="bold")
   plt.tight_layout()
   #left, bottom, width, height
   fig.subplots_adjust(bottom=0.15, top=0.90, left = 0.05, right=0.95)
   cbar_ax = fig.add_axes([0.03, 0.10, 0.94, 0.03])
   cbar=plt.colorbar(cplot, cax=cbar_ax, orientation='horizontal', ticks=cticks)
   #cbar.set_label("$T_s$$'$ / $^{\circ}$C",size=26,labelpad=-0.05)
   cbar.set_label(clabel,size=24,labelpad=-0.05)
   cbar.ax.tick_params(labelsize=24)
   pp.savefig(fig)
   pp.close()

#********************************************************************************************************
# One plot, height-month cross section
def plot_correlation(x, y, xlab, ylab, outname):

   fig = plt.figure(figsize=(8, 8))
   
   # R-squared value
   slope, intercept, r_value, p_value, std_err = ss.linregress(x, y)
   r_squared = r_value**2

   plt.text(4.1, 2.1, 'R$^2$='+str(round(Decimal(r_squared),2)), fontsize=20)
   plt.scatter(x, y)
   #plt.title(title, fontsize=20, weight='bold')
   plt.xlabel(xlab,fontsize=22)
   plt.ylabel(ylab,fontsize=22)
   plt.tick_params(axis='both', which='major', labelsize=22)
   plt.xlim([4,12])
   plt.ylim([0.8,2.2])
   plt.tight_layout()

   plt.savefig(outname)
   plt.close()


#********************************************************************************************************
# Old functions
   #map = Basemap(projection='cyl',llcrnrlat=llat,urcrnrlat=ulat,llcrnrlon=llon,urcrnrlon=ulon, fix_aspect=False)
   ## cylindrical is regular in latitude/longitude so no complicated mapping onto map coordinates
   #x, y = map(glon,glat)
   #plt_ax = fig.add_axes([0.12, 0.27, 0.83, 0.65]) # left, bottom, width, height
   #cplot=map.contourf(x,y,ibase,levs,extend="both", cmap=cols, ax=plt_ax)
   ## plot coastlines, draw label meridians and parallels.
   #map.drawcoastlines(linewidth=1,color="black")
   #map.drawparallels(np.arange(-90,100,30),labels=[1,0,0,0],fontsize=22,linewidth=0)
   #map.drawmeridians(np.arange(-180,240,60),labels=[0,0,0,1],fontsize=22,linewidth=0)
   #map.drawmapboundary()

   #cs = map.contourf(x,y,itvals.astype(int),levels=[-1,0,1],hatches=[None,'.'],colors='none') 
   #for m in range(len(itlon)-1):
   #   for n in range(len(lat)-1):
   #   #for n in range(iEQ+1):
   #      print(m, n)
   #      if itvals[n,m]:
   #         x1 = itlon[m]
   #         x2 = itlon[m+1]
   #         y1 = lat[n]
   #         y2 = lat[n+1]
   #         plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='//',linewidth=0)
   #         plt.fill([x1,x2,x2,x1],[y1,y1,y2,y2],edgecolor='grey',fill=False,hatch='\\',linewidth=0)
