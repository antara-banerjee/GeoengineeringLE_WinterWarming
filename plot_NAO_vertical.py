'''
Plot vertical profiles of trends in the North Atlantic Oscillation

-uses pre-computed first Principal Component of zonal wind (NAO index)
-set up for RCP8.5, Feedback and GEOHEAT_S simulations
-ensemble mean timeseries with ensemble uncertainty is plotted
'''

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss

#*********************************************************************************
outdir = '/Users/abanerjee/scripts/glens/output/'
npydir = '/Users/abanerjee/scripts/glens/npy_output/'
nplevel = np.load(npydir+'nplevel.npy')

#*********************************************************************************
season = 'DJF'
run='feedback'
mode='NAO'
varcode='Z3'

#*********************************************************************************
# Feedback
if run=='feedback':
   slopes = []
   N = 20
   title = '(a) GEO8.5'
   outname = 'vertical_'+mode+'-'+varcode+'_Feedback_DJF.png'
   for i in range(1,N+1):
   
      tseries = np.load(npydir+mode+'-'+varcode+'_PC_feedback_'+str(i)+'_DJF.npy')

      nyrs = tseries.shape[0]
   
      slope = np.empty([len(nplevel)])
      for ilev in range(len(nplevel)):
         slope[ilev] = ss.linregress(range(nyrs), tseries[:,ilev])[0] * 30
   
      slopes.append(slope)

#*********************************************************************************
# RCP8.5
if run=='rcp85':
   slopes = []
   N = 3
   title = '(c) RCP8.5'
   outname = 'vertical_NAO-U_RCP85_DJF.png'
   for i in range(1,N+1):
   
      #NAO = np.load(npydir+'NAO-'+varcode+'_vertical_rcp85_PC'+str(i)+'.npy')
      NAO = np.load(npydir+'NAO-'+varcode+'_PC_feedback_'+str(i)+'._DJFnpy')
      nyrs = NAO.shape[0]
   
      slope = np.empty([len(nplevel)])
      for ilev in range(len(nplevel)):
         slope[ilev] = ss.linregress(range(nyrs), NAO[:,ilev])[0] * 30
   
      slopes.append(slope)

#*********************************************************************************
# GEOHEAT
if run=='geoheats':
   slopes = []
   N = 4
   title = '(b) GEOHEAT'
   outname = 'vertical_'+mode+'-'+varcode+'_GEOHEATS_DJF.png'
   for i in range(1,N+1):
   
      NAO = np.load(npydir+'NAO-'+varcode+'_PC_geoheats_'+str(i)+'_'+season+'.npy') 
      NAO = NAO[0,:] / 65.*30.
   
      slopes.append(NAO)

#*********************************************************************************
ensmean = np.mean(np.array(slopes), axis=0)
ensstd = np.std(np.array(slopes), axis=0)
CI = 2*ensstd/np.sqrt(N)
Lperc = np.percentile(np.array(slopes), 5, axis=0) 
Uperc = np.percentile(np.array(slopes), 95, axis=0)

#*********************************************************************************
plt.figure(figsize=(5, 5), dpi=300)
plt.errorbar(ensmean, -np.log10(nplevel), xerr=CI, color='b', elinewidth=0.8, capsize=3) 
for i in range(len(nplevel)):
   plt.plot([Lperc[i],Uperc[i]], [-np.log10(nplevel[i]), -np.log10(nplevel[i])], color='k', linewidth=0.5)
#plt.errorbar(ensmean, -np.log10(nplevel), xerr=CI, color='k', elinewidth=0.8, capsize=3) 
#for i in range(N):
#   plt.scatter(np.array(slopes)[i,:], -np.log10(nplevel), color=plt.cm.Set1(i), s=10)
plt.xlabel('NAO trend / stdev per 30 years', fontsize=14)
plt.ylabel('Pressure (hPa)', fontsize=14)
plt.title(title, fontsize=16)
plt.ylim([-np.log10(1000), -np.log10(1)])
yticks = [1000,100,10,1]
plt.yticks(-np.log10(yticks),yticks)
plt.xlim([-0.8,1])
plt.axvline(x=0, color='k', linewidth=0.5, linestyle='--')
plt.tick_params(axis='both', which='major', labelsize=14)
plt.subplots_adjust(left=0.18, bottom=0.13, top=0.93, right=0.95)
plt.savefig(outdir+outname)
plt.close()

#*********************************************************************************
# END
#*********************************************************************************
