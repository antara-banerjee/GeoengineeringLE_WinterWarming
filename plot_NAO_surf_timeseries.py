#*********************************************************************************    
import cartopy.crs as ccrs                                                            
import matplotlib.pyplot as plt                                                       
import matplotlib.path as mpath                                                       
import numpy as np                                                                    
import xarray as xr                                                                   
import glob                                                                           
from cftime import DatetimeNoLeap                                                     
import scipy.stats as ss                                                              
from scipy import signal                                                              
import sys                                                                            
from eofs.standard import Eof                                                         
                                                                                      
# user modules                                                                        
import ensemble_functions                                                             
import custom_colors as ccol                                                          

#*********************************************************************************    
season = 'JJA'
run='feedback'
varcode='PSL'

#*********************************************************************************    
if run=='feedback':
   plotlett = {'DJF':'(d)','JJA':'(e)'}
elif run=='rcp85':
   plotlett = {'DJF':'(f)'}
Ndict={'feedback':20,'rcp85':3}
N = Ndict[run]
outdir="/Users/abanerjee/scripts/glens/output/"
npydir="/Users/abanerjee/scripts/glens/npy_output/"

#*********************************************************************************    
# Feedback and RCP8.5
PCs = []
for i in range(1,N+1):
   PC = np.load(npydir+'NAO-'+varcode+'_PC_'+run+'_'+str(i)+'_'+season+'.npy')
   PCs.append(PC)

print(np.array(PCs).shape)
PC_mean = np.mean(np.array(PCs), axis=0)
CI = 2*np.std(np.array(PCs), axis=0)/np.sqrt(N)

slope, intercept, r_value, p_value, stderr = ss.linregress(range(PC_mean.shape[0]), PC_mean)
print('slope = ',slope*30.)
print('CI slope = ',2*stderr*30.)

#*********************************************************************************    
# GEOHEAT_S
if season=='DJF':
   PCs = []
   for i in range(1,5):
      PC = np.load(npydir+'NAO-'+varcode+'_PC_geoheats_'+str(i)+'_'+season+'.npy')[0]
      PCs.append(PC)
   PC_mean_geoheats = np.mean(np.array(PCs), axis=0)
   CI_geoheats = 2*np.std(np.array(PCs), axis=0)/np.sqrt(4)
   print('GEOHEAT_S mean and confidence interval: ',PC_mean_geoheats,CI_geoheats)

#*********************************************************************************    
# Plot
fig = plt.figure(figsize=(8,5))
plt.plot(np.arange(2020,2095), PC_mean, color='k')
plt.fill_between(x=np.arange(2020,2095), y1=0, y2=PC_mean, where=PC_mean>0, color='r', interpolate=True)
plt.fill_between(x=np.arange(2020,2095), y1=0, y2=PC_mean, where=PC_mean<0, color='b', interpolate=True)
plt.fill_between(x=np.arange(2020,2095), y1=PC_mean-CI, y2=PC_mean+CI, color='grey', interpolate=True, alpha=0.4)
plt.plot(np.arange(2020,2095), slope*range(75)+intercept, linestyle='--', color='k')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Standardized NAO index', fontsize=14)
plt.xlim([2020,2095])
if run=='feedback':
   plt.title(plotlett[season]+' GEO8.5\nNAO index\n'+season, fontsize=18)
   if season=='DJF':
      plt.ylim([-1.2,1.2])
      plt.scatter(x=2085, y=PC_mean_geoheats, color='magenta', s=40) # geoheat
      plt.errorbar(x=2085, y=PC_mean_geoheats, yerr=CI_geoheats, color='magenta', elinewidth=2, capthick=2, capsize=5) # geoheat
   elif season=='JJA':
      plt.ylim([-1.6,1.6])
elif run=='rcp85':
   plt.title(plotlett[season]+' RCP8.5\nNAO index\n'+season, fontsize=18)
   plt.ylim([-3,3])
plt.tick_params(labelsize=14)
plt.subplots_adjust(bottom=0.12, left=0.12, top=0.82, right=0.95)
plt.savefig(outdir+'NAO-'+varcode+'_PC'+run+'_'+season+'.png')
plt.close()

#*********************************************************************************    
# END
#*********************************************************************************    
