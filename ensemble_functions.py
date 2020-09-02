import numpy as np
import scipy.stats as ss
import xarray as xr

#********************************************************************************************************
# This module contains functions to compute ensemble statistics 
#********************************************************************************************************

#********************************************************************************************************
# Ensemble mean and standard deviation
# input is array of member results, stacked on first axis
def stats(xrobjects):

   # adapted from http://xarray.pydata.org/en/stable/generated/xarray.apply_ufunc.html
   # note: this version does not stack coordinates
   dim = 'member'
   new_coord = range(len(xrobjects))

   func = lambda *x: np.stack(x, axis=-1)
   stack = xr.apply_ufunc(func, *xrobjects,
                        output_core_dims=[[dim]],
                        join='outer',
                        dataset_fill_value=np.nan)
   stack[dim] = new_coord

   ensmean = stack.mean('member')
   ensstd = stack.std('member')
  
   return (ensmean, ensstd)

#********************************************************************************************************
# Two sample t-test (two-tailed)
# ttest variable is TRUE where NOT significant
def t_test_twosample(alpha, diff, std1, std2, n1, n2):

    tstat = abs(diff)/np.sqrt((std1**2/n1)+(std2**2/n2))
    tcrit = ss.t.ppf(1-alpha/2., n1+n2-2)
    ttest = tstat < tcrit

    return ttest

#********************************************************************************************************
# One sample t-test (two-tailed)
# ttest variable is TRUE where NOT significant
def t_test_onesample(alpha, x, std, n):
    
    tstat = abs(x)/np.sqrt(std**2/n)
    tcrit = ss.t.ppf(1-alpha/2., n-1)
    ttest = tstat < tcrit

    return ttest

#********************************************************************************************************
# END 
#********************************************************************************************************
