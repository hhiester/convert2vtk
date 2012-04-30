# utility functions (visible from python).

def stringtoarr(string,NUMCHARS):
    """
stringtoarr(a, NUMCHARS)

convert a string to a character array of length NUMCHARS

@param a:  Input python string.

@param NUMCHARS:  number of characters used to represent string 
(if len(a) < NUMCHARS, it will be padded on the right with blanks).

@return: A rank 1 numpy character array of length NUMCHARS with datatype 'S1'"""
    arr = numpy.zeros(NUMCHARS,'S1')
    arr[0:len(string)] = tuple(string)
    return arr

def stringtochar(a):
    """
stringtochar(a)

convert a string array to a character array with one extra dimension

@param a:  Input numpy string array with numpy datatype 'SN', where N
is the number of characters in each string.  Will be converted to
an array of characters (datatype 'S1') of shape a.shape + (N,).

@return: A numpy character array with datatype 'S1' and shape 
a.shape + (N,), where N is the length of each string in a."""
    b = numpy.array(tuple(a.tostring().decode(default_encoding)),'S1')
    b.shape = a.shape + (a.itemsize,)
    return b

def chartostring(b):
    """
chartostring(b)

convert a character array to a string array with one less dimension.

@param b:  Input character array (numpy datatype 'S1').
Will be converted to a array of strings, where each string has a fixed
length of b.shape[-1] characters.

@return: A numpy string array with datatype 'SN' and shape b.shape[:-1],
where N=b.shape[-1]."""
    bs = b.tostring().decode(default_encoding)
    slen = b.shape[-1]
    a = numpy.array([bs[n1:n1+slen] for n1 in range(0,len(bs),slen)],'S'+repr(slen))
    a.shape = b.shape[:-1]
    return a

def date2num(dates,units,calendar='standard'):
    """
date2num(dates,units,calendar='standard')

Return numeric time values given datetime objects. The units
of the numeric time values are described by the L{units} argument
and the L{calendar} keyword. The datetime objects must
be in UTC with no time-zone offset.  If there is a 
time-zone offset in C{units}, it will be applied to the
returned numeric values.

Like the matplotlib C{date2num} function, except that it allows
for different units and calendars.  Behaves the same if
C{units = 'days since 0001-01-01 00:00:00'} and 
C{calendar = 'proleptic_gregorian'}.

@param dates: A datetime object or a sequence of datetime objects.
 The datetime objects should not include a time-zone offset.

@param units: a string of the form C{'B{time units} since B{reference time}}'
 describing the time units. B{C{time units}} can be days, hours, minutes
 or seconds.  B{C{reference time}} is the time origin. A valid choice
 would be units=C{'hours since 1800-01-01 00:00:00 -6:00'}.

@param calendar: describes the calendar used in the time calculations. 
 All the values currently defined in the U{CF metadata convention 
 <http://cf-pcmdi.llnl.gov/documents/cf-conventions/>} are supported.
 Valid calendars C{'standard', 'gregorian', 'proleptic_gregorian'
 'noleap', '365_day', '360_day', 'julian', 'all_leap', '366_day'}.
 Default is C{'standard'}, which is a mixed Julian/Gregorian calendar.

@return: a numeric time value, or an array of numeric time values.

The maximum resolution of the numeric time values is 1 second.
    """
    cdftime = netcdftime.utime(units,calendar=calendar)
    return cdftime.date2num(dates)

def num2date(times,units,calendar='standard'):
    """
num2date(times,units,calendar='standard')

Return datetime objects given numeric time values. The units
of the numeric time values are described by the C{units} argument
and the C{calendar} keyword. The returned datetime objects represent 
UTC with no time-zone offset, even if the specified 
C{units} contain a time-zone offset.

Like the matplotlib C{num2date} function, except that it allows
for different units and calendars.  Behaves the same if
C{units = 'days since 001-01-01 00:00:00'} and 
C{calendar = 'proleptic_gregorian'}.

@param times: numeric time values. Maximum resolution is 1 second.

@param units: a string of the form C{'B{time units} since B{reference time}}'
describing the time units. B{C{time units}} can be days, hours, minutes
or seconds.  B{C{reference time}} is the time origin. A valid choice
would be units=C{'hours since 1800-01-01 00:00:00 -6:00'}.

@param calendar: describes the calendar used in the time calculations. 
All the values currently defined in the U{CF metadata convention 
<http://cf-pcmdi.llnl.gov/documents/cf-conventions/>} are supported.
Valid calendars C{'standard', 'gregorian', 'proleptic_gregorian'
'noleap', '365_day', '360_day', 'julian', 'all_leap', '366_day'}.
Default is C{'standard'}, which is a mixed Julian/Gregorian calendar.

@return: a datetime instance, or an array of datetime instances.

The datetime instances returned are 'real' python datetime 
objects if the date falls in the Gregorian calendar (i.e. 
C{calendar='proleptic_gregorian'}, or C{calendar = 'standard'} or C{'gregorian'}
and the date is after 1582-10-15). Otherwise, they are 'phony' datetime 
objects which support some but not all the methods of 'real' python
datetime objects.  This is because the python datetime module cannot
the uses the C{'proleptic_gregorian'} calendar, even before the switch
occured from the Julian calendar in 1582. The datetime instances
do not contain a time-zone offset, even if the specified C{units}
contains one.
    """
    cdftime = netcdftime.utime(units,calendar=calendar)
    return cdftime.num2date(times)

def date2index(dates, nctime, calendar=None, select='exact'):
    """
date2index(dates, nctime, calendar=None, select='exact')

Return indices of a netCDF time variable corresponding to the given dates.

@param dates: A datetime object or a sequence of datetime objects.
The datetime objects should not include a time-zone offset.

@param nctime: A netCDF time variable object. The nctime object must have a
C{units} attribute.

@param calendar: Describes the calendar used in the time calculation.
Valid calendars C{'standard', 'gregorian', 'proleptic_gregorian'
'noleap', '365_day', '360_day', 'julian', 'all_leap', '366_day'}.
Default is C{'standard'}, which is a mixed Julian/Gregorian calendar
If C{calendar} is None, its value is given by C{nctime.calendar} or
C{standard} if no such attribute exists.

@param select: C{'exact', 'before', 'after', 'nearest'}
The index selection method. C{exact} will return the indices perfectly 
matching the dates given. C{before} and C{after} will return the indices 
corresponding to the dates just before or just after the given dates if 
an exact match cannot be found. C{nearest} will return the indices that 
correspond to the closest dates. 
      
@return: an index (indices) of the netCDF time variable corresponding
to the given datetime object(s).
    """
    return netcdftime.date2index(dates, nctime, calendar, select)

def getlibversion():
    """
getlibversion()

returns a string describing the version of the netcdf library
used to build the module, and when it was built.
    """
    cdef char *libstring
    libstring = nc_inq_libvers()
    return libstring.decode('ascii')

class MFDataset(Dataset): 
    """
MFDataset(self, files, check=False, exclude=[])

Class for reading multi-file netCDF Datasets, making variables
spanning multiple files appear as if they were in one file.

Datasets must be in C{NETCDF4_CLASSIC, NETCDF3_CLASSIC or NETCDF3_64BIT}
format (C{NETCDF4} Datasets won't work).

Adapted from U{pycdf <http://pysclint.sourceforge.net/pycdf>} by Andre Gosselin.

Example usage:

>>> import numpy
>>> # create a series of netCDF files with a variable sharing
>>> # the same unlimited dimension.
>>> for nfile in range(10):
>>>     f = Dataset('mftest'+repr(nfile)+'.nc','w')
>>>     f.createDimension('x',None)
>>>     x = f.createVariable('x','i',('x',))
>>>     x[0:10] = numpy.arange(nfile*10,10*(nfile+1))
>>>     f.close()
>>> # now read all those files in at once, in one Dataset.
>>> f = MFDataset('mftest*nc')
>>> print f.variables['x'][:]
[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49
 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74
 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99]
    """

    def __init__(self, files, check=False, exclude=[]):
        """
Open a Dataset spanning multiple files, making it look as if it was a 
single file. Variables in the list of files that share the same unlimited 
dimension are aggregated. 

Adapted from U{pycdf <http://pysclint.sourceforge.net/pycdf>} by Andre Gosselin.

Usage:

nc = MFDataset(files, check=False, exclude=[])

@param files: either a sequence of netCDF files or a string with a 
wildcard (converted to a sorted list of files using glob)  The first file 
in the list will become the "master" file, defining all the record 
variables (variables with an unlimited dimension) which may span 
subsequent files. Attribute access returns attributes only from "master" 
file. The files are always opened in read-only mode.

@param check: True if you want to do consistency checking to ensure the 
correct variables structure for all of the netcdf files.  Checking makes 
the initialization of the MFDataset instance much slower. Default is 
False.

@param exclude: A list of variable names to exclude from aggregation. 
Default is an empty list.
       """

        # Open the master file in the base class, so that the CDFMF instance
        # can be used like a CDF instance.
        if isinstance(files, str):
            if files.startswith('http'):
                msg='cannot using file globbing for remote (OPeNDAP) datasets'
                raise ValueError(msg)
            else:
                files = sorted(glob(files))
        
        master = files[0]

        # Open the master again, this time as a classic CDF instance. This will avoid
        # calling methods of the CDFMF subclass when querying the master file.
        cdfm = Dataset(master)
        # copy attributes from master.
        for name, value in cdfm.__dict__.items():
            self.__dict__[name] = value

        # Make sure the master defines an unlimited dimension.
        unlimDimId = None
        for dimname,dim in cdfm.dimensions.items():
            if dim.isunlimited():
                unlimDimId = dim
                unlimDimName = dimname
        if unlimDimId is None:
            raise IOError("master dataset %s does not have an unlimited dimension" % master)

        # Get info on all record variables defined in the master.
        # Make sure the master defines at least one record variable.
        masterRecVar = {}
        for vName,v in cdfm.variables.items():
            # skip variables specified in exclude list.
            if vName in exclude: continue
            dims = v.dimensions
            shape = v.shape
            type = v.dtype
            # Be carefull: we may deal with a scalar (dimensionless) variable.
            # Unlimited dimension always occupies index 0.
            if (len(dims) > 0 and unlimDimName == dims[0]):
                masterRecVar[vName] = (dims, shape, type)
        if len(masterRecVar) == 0:
            raise IOError("master dataset %s does not have any record variable" % master)

        # Create the following:
        #   cdf       list of Dataset instances
        #   cdfVLen   list unlimited dimension lengths in each CDF instance
        #   cdfRecVar dictionnary indexed by the record var names; each key holds
        #             a list of the corresponding Variable instance, one for each
        #             cdf file of the file set
        cdf = [cdfm]
        self._cdf = cdf        # Store this now, because dim() method needs it
        cdfVLen = [len(unlimDimId)]
        cdfRecVar = {}
        for v in masterRecVar.keys():
            cdfRecVar[v] = [cdfm.variables[v]]
        
        # Open each remaining file in read-only mode.
        # Make sure each file defines the same record variables as the master
        # and that the variables are defined in the same way (name, shape and type)
        for f in files[1:]:
            part = Dataset(f)
            varInfo = part.variables
            for v in masterRecVar.keys():
                if check:
                    # Make sure master rec var is also defined here.
                    if v not in varInfo.keys():
                        raise IOError("record variable %s not defined in %s" % (v, f))

                    # Make sure it is a record var.
                    vInst = part.variables[v]
                    if not part.dimensions[vInst.dimensions[0]].isunlimited():
                        raise MFDataset("variable %s is not a record var inside %s" % (v, f))

                    masterDims, masterShape, masterType = masterRecVar[v][:3]
                    extDims, extShape, extType = varInfo[v][:3]
                    extDims = varInfo[v].dimensions
                    extShape = varInfo[v].shape
                    extType = varInfo[v].dtype
                    # Check that dimension names are identical.
                    if masterDims != extDims:
                        raise IOError("variable %s : dimensions mismatch between "
                                       "master %s (%s) and extension %s (%s)" %
                                       (v, master, masterDims, f, extDims))

                    # Check that the ranks are identical, and the dimension lengths are
                    # identical (except for that of the unlimited dimension, which of
                    # course may vary.
                    if len(masterShape) != len(extShape):
                        raise IOError("variable %s : rank mismatch between "
                                       "master %s (%s) and extension %s (%s)" %
                                       (v, master, len(masterShape), f, len(extShape)))
                    if masterShape[1:] != extShape[1:]:
                        raise IOError("variable %s : shape mismatch between "
                                       "master %s (%s) and extension %s (%s)" %
                                       (v, master, masterShape, f, extShape))

                    # Check that the data types are identical.
                    if masterType != extType:
                        raise IOError("variable %s : data type mismatch between "
                                       "master %s (%s) and extension %s (%s)" %
                                       (v, master, masterType, f, extType))

                    # Everythig ok.
                    cdfRecVar[v].append(vInst)
                else:
                    # No making sure of anything -- assume this is ok..
                    vInst = part.variables[v]
                    cdfRecVar[v].append(vInst)

            cdf.append(part)
            cdfVLen.append(len(part.dimensions[unlimDimName]))

        # Attach attributes to the MFDataset instance.
        # A local __setattr__() method is required for them.
        self._files = files            # list of cdf file names in the set
        self._cdfVLen = cdfVLen              # list of unlimited lengths
        self._cdfTLen = sum(cdfVLen) # total length
        self._cdfRecVar = cdfRecVar          # dictionary of Variable instances for all
                                             # the record variables
        self._dims = cdfm.dimensions
        self._grps = cdfm.groups
        for dimname, dim in self._dims.items():
            if dim.isunlimited():
                self._dims[dimname] = _Dimension(dimname, dim, self._cdfVLen, self._cdfTLen)
        self._vars = cdfm.variables
        for varname,var in self._vars.items():
            if varname in self._cdfRecVar.keys():
                self._vars[varname] = _Variable(self, varname, var, unlimDimName)
        self._file_format = []
        for dset in self._cdf:
            if dset.file_format == 'NETCDF4':
                raise ValueError('MFNetCDF4 only works with NETCDF3_CLASSIC, NETCDF3_64BIT and NETCDF4_CLASSIC formatted files, not NETCDF4')
            self._file_format.append(dset.file_format)

    def __setattr__(self, name, value):
        """override base class attribute creation"""
        self.__dict__[name] = value

    def __getattribute__(self, name):
        if name in ['variables','dimensions','file_format','groups']: 
            if name == 'dimensions': return self._dims
            if name == 'variables': return self._vars
            if name == 'file_format': return self._file_format
            if name == 'groups': return self._grps
        else:
            return Dataset.__getattribute__(self, name)

    def ncattrs(self):
        return self._cdf[0].__dict__.keys()

    def close(self):
        for dset in self._cdf:
            dset.close()

    def __str__(self):
        ncdump = ['%r\n' % type(self)]
        dimnames = tuple([str(dimname) for dimname in self.dimensions.keys()])
        varnames = tuple([str(varname) for varname in self.variables.keys()])
        grpnames = ()
        if self.path == '/':
            ncdump.append('root group (%s file format):\n' % self.file_format)
        else:
            ncdump.append('group %s:\n' % self.path)
        attrs = ['    %s: %s\n' % (name,self.__dict__[name]) for name in\
                self.ncattrs()]
        ncdump = ncdump + attrs
        ncdump.append('    dimensions = %s\n' % str(dimnames))
        ncdump.append('    variables = %s\n' % str(varnames))
        ncdump.append('    groups = %s\n' % str(grpnames))
        return ''.join(ncdump)

class _Dimension(object):
    def __init__(self, dimname, dim, dimlens, dimtotlen):
        self.dimlens = dimlens
        self.dimtotlen = dimtotlen
        self._name = dimname
    def __len__(self):
        return self.dimtotlen
    def isunlimited(self):
        return True
    def __str__(self):
        if self.isunlimited():
            return repr(type(self))+" (unlimited): name = '%s', size = %s\n" % (self._name,len(self))
        else:
            return repr(type(self))+": name = '%s', size = %s\n" % (self._name,len(self))

class _Variable(object):
    def __init__(self, dset, varname, var, recdimname):
        self.dimensions = var.dimensions 
        self._dset = dset
        self._grp = dset
        self._mastervar = var
        self._recVar = dset._cdfRecVar[varname]
        self._recdimname = recdimname
        self._recLen = dset._cdfVLen
        self.dtype = var.dtype
        self._name = var._name
        # copy attributes from master.
        for name, value in var.__dict__.items():
            self.__dict__[name] = value
    def typecode(self):
        return self.dtype
    def ncattrs(self):
        return self._mastervar.__dict__.keys()
    def __getattr__(self,name):
        if name == 'shape': return self._shape()
        if name == 'ndim': return len(self._shape())
        try:
            return self.__dict__[name]
        except:
            raise AttributeError(name)
    def __str__(self):
        ncdump_var = ['%r\n' % type(self)]
        dimnames = tuple([str(dimname) for dimname in self.dimensions])
        attrs = ['    %s: %s\n' % (name,self.__dict__[name]) for name in\
                self.ncattrs()]
        ncdump_var.append('%s %s%s\n' %\
        (self.dtype,self._name,dimnames))
        ncdump_var = ncdump_var + attrs
        unlimdims = []
        for dimname in self.dimensions:
            dim = _find_dim(self._grp, dimname)
            if dim.isunlimited():
                unlimdims.append(str(dimname))
        ncdump_var.append('unlimited dimensions = %s\n' % repr(tuple(unlimdims)))
        ncdump_var.append('current size = %s\n' % repr(self.shape))
        return ''.join(ncdump_var)
    def __len__(self):
        return self._shape()[0]
    def _shape(self):
        recdimlen = len(self._dset.dimensions[self._recdimname])
        return (recdimlen,) + self._mastervar.shape[1:]
    def set_auto_maskandscale(self,val):
        for v in self._recVar:
            v.set_auto_maskandscale(val)
    def __getitem__(self, elem):
        """Get records from a concatenated set of variables."""

        # This special method is used to index the netCDF variable
        # using the "extended slice syntax". The extended slice syntax
        # is a perfect match for the "start", "count" and "stride"
        # arguments to the nc_get_var() function, and is much more easy
        # to use.
        start, count, stride, put_ind =\
        _StartCountStride(elem, self.shape)
        datashape = _out_array_shape(count)
        data = ma.empty(datashape, dtype=self.dtype)
        
        # Determine which dimensions need to be squeezed
        # (those for which elem is an integer scalar).
        # The convention used is that for those cases, 
        # put_ind for this dimension is set to -1 by _StartCountStride.
        squeeze = data.ndim * [slice(None),]
        for i,n in enumerate(put_ind.shape[:-1]):
            if n == 1 and put_ind[...,i].ravel()[0] == -1:
                squeeze[i] = 0

        # Reshape the arrays so we can iterate over them. 
        strt = start.reshape((-1, self.ndim or 1))
        cnt = count.reshape((-1, self.ndim or 1))
        strd = stride.reshape((-1, self.ndim or 1))
        put_ind = put_ind.reshape((-1, self.ndim or 1))

        # Fill output array with data chunks. 
        # Number of variables making up the MFVariable.Variable.
        nv = len(self._recLen)
        for (start,count,stride,ind) in zip(strt, cnt, strd, put_ind):
            # make sure count=-1 becomes count=1
            count = [abs(cnt) for cnt in count]
            if (numpy.array(stride) < 0).any():
                raise IndexError('negative strides not allowed when slicing MFVariable Variable instance')
            # Start, stop and step along 1st dimension, eg the unlimited
            # dimension.
            sta = start[0]
            step = stride[0]
            stop = sta + count[0] * step
            
            # Build a list representing the concatenated list of all records in
            # the MFVariable variable set. The list is composed of 2-elem lists
            # each holding:
            #  the record index inside the variables, from 0 to n
            #  the index of the Variable instance to which each record belongs
            idx = []    # list of record indices
            vid = []    # list of Variable indices
            for n in range(nv):
                k = self._recLen[n]     # number of records in this variable
                idx.extend(range(k))
                vid.extend([n] * k)

            # Merge the two lists to get a list of 2-elem lists.
            # Slice this list along the first dimension.
            lst = list(zip(idx, vid)).__getitem__(slice(sta, stop, step))

            # Rebuild the slicing expression for dimensions 1 and ssq.
            newSlice = [slice(None, None, None)]
            for n in range(1, len(start)):   # skip dimension 0
                s = slice(start[n],start[n] + count[n] * stride[n], stride[n])
                newSlice.append(s)
                
            # Apply the slicing expression to each var in turn, extracting records
            # in a list of arrays.
            lstArr = []
            ismasked = False
            for n in range(nv):
                # Get the list of indices for variable 'n'.
                idx = [i for i,numv in lst if numv == n]
                if idx:
                    # Rebuild slicing expression for dimension 0.
                    newSlice[0] = slice(idx[0], idx[-1] + 1, step)
                    # Extract records from the var, and append them to a list
                    # of arrays.
                    dat = Variable.__getitem__(self._recVar[n],tuple(newSlice))
                    if hasattr(dat,'mask') and not ismasked:
                        ismasked=True
                        fill_value = dat.fill_value
                    lstArr.append(dat)
            if ismasked:
                lstArr = ma.concatenate(lstArr)
            else:
                lstArr = numpy.concatenate(lstArr)
            if lstArr.dtype != data.dtype: data = data.astype(lstArr.dtype)
            # sometimes there are legitimate singleton dimensions, in which
            # case the array shapes won't conform. If so, a ValueError will
            # result, and no squeeze will be done.
            try:
                data[tuple(ind)] = lstArr.squeeze()
            except ValueError:
                data[tuple(ind)] = lstArr

        # Remove extra singleton dimensions. 
        data = data[tuple(squeeze)]

        # if no masked elements, return numpy array.
        if hasattr(data,'mask') and not data.mask.any():
           data = data.filled()
        
        return data


class MFTime(_Variable):
    """
MFTime(self, time, units=None)

Class providing an interface to a MFDataset time Variable by imposing a unique common
time unit to all files.

Example usage:

>>> import numpy
>>> f1 = Dataset('mftest_1.nc','w', format='NETCDF4_CLASSIC')
>>> f2 = Dataset('mftest_2.nc','w', format='NETCDF4_CLASSIC')
>>> f1.createDimension('time',None)
>>> f2.createDimension('time',None)
>>> t1 = f1.createVariable('time','i',('time',))
>>> t2 = f2.createVariable('time','i',('time',))
>>> t1.units = 'days since 2000-01-01'
>>> t2.units = 'days since 2000-02-01'
>>> t1.calendar = 'standard'
>>> t2.calendar = 'standard'
>>> t1[:] = numpy.arange(31)
>>> t2[:] = numpy.arange(30)
>>> f1.close()
>>> f2.close()
>>> # Read the two files in at once, in one Dataset.
>>> f = MFDataset('mftest*nc')
>>> t = f.variables['time']
>>> print t.units
days since 2000-01-01
>>> print t[32] # The value written in the file, inconsistent with the MF time units.
1
>>> T = MFTime(t)
>>> print T[32]                        
32                           
    """
    
    def __init__(self, time, units=None):
        """
Create a time Variable with units consistent across a multifile 
dataset.

@param time: Time variable from a MFDataset. 

@param units: Time units, for example, 'days since 1979-01-01'. If None, use
the units from the master record. 
        """
        import datetime
        self.__time = time
        
        # copy attributes from master time variable.
        for name, value in time.__dict__.items():
            self.__dict__[name] = value
           
        
        # Check that calendar is the same in all files.
        if len(set([t.calendar for t in self._recVar])) > 1:
            raise ValueError('MFTime requires that the same time calendar is used by all files.')
 
        # Override units if units is specified.
        self.units = units or time.units
        
        # Reference date to compute the difference between different time units. 
        ref_date = datetime.datetime(1900,1,1)
        ref_num = date2num(ref_date, self.units, self.calendar)
        
        # Create delta vector: delta = ref_num(ref_date) - num(ref_date)
        # So that ref_num(date) = num(date) + delta 
        self.__delta = numpy.empty(len(self), time.dtype)
        
        i0 = 0; i1 = 0
        for i,v in enumerate(self._recVar):
            n = self._recLen[i] # Length of time vector.
            num = date2num(ref_date, v.units, self.calendar)
            i1 += n            
            self.__delta[i0:i1] = ref_num - num
            i0 += n
        
                
    def __getitem__(self, elem):
        return self.__time[elem] + self.__delta[elem]
