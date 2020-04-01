import numpy as np
import netCDF4 as ncdf
import datetime

#********************************************************************************************************
# GET_VARS: gets any number of variables from a netcdf file object
def get_ncmod(path):

   # load netcdf file
   ncmod = ncdf.Dataset(path,'r')

   return ncmod

#********************************************************************************************************
# GET_DIMS: gets any number of dimensions from a netcdf file object
def get_dims(ncmod, **dims):

   return_dims = ()
   # extract dimensions
   if 'lonname' in dims:
      lon=ncmod.variables[dims['lonname']][:] 
      return_dims = return_dims + (lon,)
   if 'latname' in dims:
      lat=ncmod.variables[dims['latname']][:] 
      return_dims = return_dims + (lat,)
   if 'hgtname' in dims:
      hgt=ncmod.variables[dims['hgtname']][:] 
      return_dims = return_dims + (hgt,)
   if 'timname' in dims:
      tim=ncmod.variables[dims['timname']][:] 
      return_dims = return_dims + (tim,)

   return return_dims

#********************************************************************************************************
# GET_VARS: gets any number of variables from a netcdf file object
def get_vars(ncmod, *vars):

   return_vars = ()
   # extract variables
   for xvar in vars:
      ncvar = np.array(ncmod.variables[xvar][:])
      return_vars = return_vars + (ncvar,)

   return return_vars

#********************************************************************************************************
# GET_VARS_SLICE: as above but slices variable in case there are memory issues! Change slicing as necessary.
# 2D
def get_vars_slice_tim2D(ncmod, tim0, tim1, *vars):

   return_vars = ()
   # extract variables
   for xvar in vars:
      ncvar = np.array(ncmod.variables[xvar][tim0:tim1,:,:])
      return_vars = return_vars + (ncvar,)

   return return_vars

# 3D
def get_vars_slice_tim3D(ncmod, tim0, tim1, *vars):

   return_vars = ()
   # extract variables
   for xvar in vars:
      ncvar = np.array(ncmod.variables[xvar][tim0:tim1,:,:,:])
      return_vars = return_vars + (ncvar,)

   return return_vars

#********************************************************************************************************
# Write to netcdf file
def write_file(ncmod, outname, **dims):

   writefile = ncdf.Dataset(outname, 'w', format='NETCDF4')
   #writefile = ncdf.Dataset(outname, 'w', format='NETCDF3_CLASSIC')

   # extract dimensions
   if 'lonname' in dims:
      lon = ncmod.variables[dims['lonname']][:] 
      print(lon.dtype)
      writefile.createDimension(dims['lonname'], len(lon))
      writefile_dim = writefile.createVariable(dims['lonname'], lon.dtype ,(dims['lonname'],))
      #writefile_dim = writefile.createVariable(dims['lonname'], 'f4' ,(dims['lonname'],))
      for ncattr in ncmod.variables[dims['lonname']].ncattrs():
         writefile_dim.setncattr(ncattr, ncmod.variables[dims['lonname']].getncattr(ncattr))
      if 'lonvalue' in dims:
         writefile.variables[dims['lonname']][:] = dims['lonvalue']
      else:
         writefile.variables[dims['lonname']][:] = lon 
   if 'latname' in dims:
      lat = ncmod.variables[dims['latname']][:] 
      writefile.createDimension(dims['latname'], len(lat))
      writefile_dim = writefile.createVariable(dims['latname'], lat.dtype,(dims['latname'],))
      #writefile_dim = writefile.createVariable(dims['latname'], 'f4',(dims['latname'],))
      for ncattr in ncmod.variables[dims['latname']].ncattrs():
         writefile_dim.setncattr(ncattr, ncmod.variables[dims['latname']].getncattr(ncattr))
      if 'latvalue' in dims:
         writefile.variables[dims['latname']][:] = dims['latvalue']
      else:
         writefile.variables[dims['latname']][:] = lat
   if 'hgtname' in dims:
      hgt = ncmod.variables[dims['hgtname']][:] 
      writefile.createDimension(dims['hgtname'], len(hgt))
      writefile_dim = writefile.createVariable(dims['hgtname'], hgt.dtype,(dims['hgtname'],))
      #writefile_dim = writefile.createVariable(dims['hgtname'], 'f4',(dims['hgtname'],))
      for ncattr in ncmod.variables[dims['hgtname']].ncattrs():
         writefile_dim.setncattr(ncattr, ncmod.variables[dims['hgtname']].getncattr(ncattr))
      if 'hgtvalue' in dims:
         writefile.variables[dims['hgtname']][:] = dims['hgtvalue']
      else:
         writefile.variables[dims['hgtname']][:] = hgt

   if 'timname' in dims:
      tim = ncmod.variables[dims['timname']][:] 
      print(tim.dtype)
      #writefile.createDimension(dims['timname'], len(tim))
      writefile.createDimension(dims['timname'], None)
      writefile_dim = writefile.createVariable(dims['timname'], tim.dtype,(dims['timname'],))
      #writefile_dim = writefile.createVariable(dims['timname'], (dims['timname'],), datatype='float64')
      if 'timvalue' in dims:
          # assume given in years
          values = map(lambda x: datetime.datetime(x,1,1,0,0), dims['timvalue'])
          strvalues = map(lambda x: (datetime.datetime(x,1,1,0,0)).strftime("%Y-%m-%d %H:%M"), dims['timvalue'])
          calendar = 'gregorian'
          units = 'hours since 1900-01-01 00:00:00.0'
          writefile_dim[:] = ncdf.date2num(values, units=units, calendar=calendar)
          [x.strftime("%Y-%m-%d %H:%M") for x in ncdf.num2date(writefile_dim[:], units=units, calendar=calendar)]
          writefile_dim.setncatts({'long_name':'time','units':'hours since 1900-01-01 00:00:00.0','calendar':'gregorian'})
          #writefile.variables[dims['timname']][:] = ncdf.date2num(dims['timvalue'], units=units, calendar=calendar)
          #writefile.setncatts({
      else:
         for ncattr in ncmod.variables[dims['timname']].ncattrs():
            writefile_dim.setncattr(ncattr, ncmod.variables[dims['timname']].getncattr(ncattr))
         #writefile.variables[dims['timname']][:] = tim

      return writefile
