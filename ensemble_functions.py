import numpy as np
import scipy.stats as ss
import xarray as xr
#plt.ioff()

def user_addcyclic(*arr,**kwargs):
    """
    Adds cyclic (wraparound) points in longitude to one or several arrays,
    the last array being longitudes in degrees. e.g.
   ``data1out, data2out, lonsout = addcyclic(data1,data2,lons)``
    ==============   ====================================================
    Keywords         Description
    ==============   ====================================================
    axis             the dimension representing longitude (default -1,
                     or right-most)
    cyclic           width of periodic domain (default 360)
    ==============   ====================================================
    """
    # get (default) keyword arguments
    axis = kwargs.get('axis',-1)
    cyclic = kwargs.get('cyclic',360)
    # define functions
    def _addcyclic(a):
        """addcyclic function for a single data array"""
        npsel = np.ma if np.ma.is_masked(a) else np
        slicer = [slice(None)] * np.ndim(a)
        try:
            slicer[axis] = slice(0, 1)
        except IndexError:
            raise ValueError('The specified axis does not correspond to an '
                    'array dimension.')
        return npsel.concatenate((a,a[slicer]),axis=axis)
    def _addcyclic_lon(a):
        """addcyclic function for a single longitude array"""
        # select the right numpy functions
        npsel = np.ma if np.ma.is_masked(a) else np
        # get cyclic longitudes
        clon = (np.take(a,[0],axis=axis)
                + cyclic * np.sign(np.diff(np.take(a,[0,-1],axis=axis),axis=axis)))
        # ensure the values do not exceed cyclic
        clonmod = npsel.where(clon<=cyclic,clon,np.mod(clon,cyclic))
        return npsel.concatenate((a,clonmod),axis=axis)
    # process array(s)
    if len(arr) == 1:
        return _addcyclic_lon(arr[-1])
    else:
        return list(map(_addcyclic,arr[:-1])) + [_addcyclic_lon(arr[-1])]

#********************************************************************************************************
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
# ttest variable is TRUE where NOT significant
def t_test(alpha, diff, std1, std2, n1, n2):
    
    tstat = diff/np.sqrt((std1**2/n1)+(std2**2/n2))
    tcrit = ss.t.ppf(1-alpha/2., n1+n2-2)#; print slope, std_err, tscore, tcrit
    ttest = tstat < tcrit

    return ttest

#********************************************************************************************************
# ttest variable is TRUE where NOT significant
def t_test_onesample(alpha, x, std, n):
    
    tstat = x/np.sqrt(std**2/n)
    tcrit = ss.t.ppf(1-alpha/2., n-1)#; print slope, std_err, tscore, tcrit
    ttest = tstat < tcrit

    return ttest
