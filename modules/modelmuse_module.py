def convert( core ):
    print "Converting the Hycom Z level file to vtk..."
    print "ibegin = ", core.ibegin
    print "iend = ", core.iend
    print "jbegin = ", core.jbegin
    print "jend = ", core.jend
    print "kbegin = ", core.kbegin
    print "kend = ", core.kend

    if core.vector_flag == True:
        ncVarsU = core.datau.variables
        ncVarsV = core.datav.variables
        dimVars = core.datau.dimensions
    else:
        ncVars = core.data.variables
        dimVars = core.data.dimensions
    args = core.variables
    if 'X' in dimVars:
        lenX = len(dimVars['X'])
    elif 'Longitude' in dimVars:
        lenX = len(dimVars['Longitude'])
    else:
        core.sys.exit("ERROR: X-dimension/Longitude variable name not recognized")
    if 'Y' in dimVars:
        lenY = len(dimVars['Y'])
    elif 'Latitude' in dimVars:
        lenY = len(dimVars['Latitude'])
    else:
        core.sys.exit("ERROR: Y-dimension/Latitude variable name not recognized")
    if 'Depth' in dimVars:
        lenZ = len(dimVars['Depth'])
    elif 'Z' in dimVars:
        lenZ = len(dimVars['Z'])
    else:
        core.sys.exit("ERROR: Z-dimension/Depth variable name not recognized")

    # Set up the x slicing range
    if (core.ibegin == 'None' and core.iend == 'None') \
        or (core.ibegin == 'None' and core.iend == lenX) \
        or (core.ibegin == 0 and core.iend == 'None') \
        or (core.ibegin == 0 and core.iend == lenX):
        ibeg = 0
        nX = lenX
        iend = nX
    elif (core.ibegin == 'None' and core.iend != 'None'):
        ibeg = 0
        iend = int(core.iend)+1
        nX = iend
    elif (core.iend == 'None' and core.ibegin != 'None'):
        ibeg = int(core.ibegin)
        nX = lenX
        iend = nX
    elif core.iend == core.ibegin:
        ibeg = int(core.ibegin)
        iend = int(core.iend)+1
        nX = 1
    else:
        ibeg = int(core.ibegin)
        iend = int(core.iend)+1
        nX = iend-ibeg


    # Set up the y slicing range
    if (core.jbegin == 'None' and core.jend == 'None') \
        or (core.jbegin == 'None' and core.jend == lenY) \
        or (core.jbegin == 0 and core.jend == 'None') \
        or (core.jbegin == 0 and core.jend == lenY):
        jbeg = 0
        nY = lenY
        jend = nY
    elif (core.jbegin == 'None' and core.jend != 'None'):
        jbeg = 0
        jend = int(core.jend)+1
        nY = jend
    elif (core.jend == 'None' and core.jbegin != 'None'):
        jbeg = int(core.jbegin)
        nY = lenY
        jend = nY
    elif core.jend == core.jbegin:
        jbeg = int(core.jbegin)
        jend = int(core.jend)+1
        nY = 1
    else:
        jbeg = int(core.jbegin)
        jend = int(core.jend)+1
        nY = jend-jbeg


    # Set up the z slicing range
    if (core.kbegin == 'None' and core.kend == 'None') \
        or (core.kbegin == 'None' and core.kend == lenZ) \
        or (core.kbegin == 0 and core.kend == 'None') \
        or (core.kbegin == 0 and core.kend == lenZ):
        kbeg = 0
        nZ = lenZ
        kend = nZ
    elif (core.kbegin == 'None' and core.kend != 'None'):
        kbeg = 0
        kend = int(core.kend)+1
        nZ = kend
    elif (core.kend == 'None' and core.kbegin != 'None'):
        kbeg = int(core.kbegin)
        nZ = lenZ
        kend = nZ
    elif core.kend == core.kbegin:
        kbeg = int(core.kbegin)
        kend = int(core.kend)+1
        nZ = 1
    else:
        kbeg = int(core.kbegin)
        kend = int(core.kend)+1
        nZ = kend-kbeg


    # Set up the time range
    if core.time_begin == 'None' and core.time_end == 'None':
        beg_time = 0
        end_time = len(dimVars['MT'])
        time = end_time-beg_time
    elif core.time_begin == 'None':
        beg_time = 0
        end_time = core.time_end
        time = end_time-beg_time
    elif core.time_end == 'None':
        beg_time = core.time_begin
        end_time = len(dimVars['MT'])
        time = end_time-beg_time
    else:
        beg_time = core.time_begin
        end_time = len(dimVars['MT'])
        time = end_time-beg_time

    print "ibegin = ", ibeg
    print "iend = ", iend
    print "jbegin = ", jbeg
    print "jend = ", jend
    print "kbegin = ", kbeg
    print "kend = ", kend
    print "nX = ", nX
    print "nY = ", nY
    print "nZ = ", nZ
                

    # Make the variables before the grid. This saves the user time if their
    # input values are bad
    vars = []
    if core.vector_flag == True:
        for t in xrange(beg_time,end_time):
            print "what"
            if 'u' in ncVarsU:
                udata = ncVarsU['u'][t,kbeg:kend,jbeg:jend,ibeg:iend]
            else:
                core.sys.exit( "ERROR: The variable \'u\' is not in the file '"+core.input_filename_u+"'" )
            print "is"
            if isinstance(udata, core.np.ma.MaskedArray):
                # Use the mask to change all masked elements to NaNs
                udata = udata.filled(core.np.nan)
            if not isinstance( udata, core.np.ndarray ):
                core.sys.exit( "ERROR: UData is not of type numpy.ndarray" )
            print "taking"
            if 'v' in ncVarsV:
                vdata = ncVarsU['v'][t,kbeg:kend,jbeg:jend,ibeg:iend]
            else:
                core.sys.exit("ERROR: The variable \'v\' is not in the file '"+core.input_filename_v+"'")
            print "so"
            if isinstance(vdata, core.np.ma.MaskedArray):
                # Use the mask to change all masked elements to NaNs
                vdata = vdata.filled(core.np.nan)
            print "long??"
            if not isinstance( vdata, core.np.ndarray ):
                core.sys.exit( "ERROR: VData is not of type numpy.ndarray" )
            print "slicing u"
            udata_slice = udata.flatten().tolist()  
            print "slicing v"
            vdata_slice = vdata.flatten().tolist()  
            data = []
            print " combining slices"
            for i in xrange( len(udata_slice) ):
                data.append( udata_slice[i] )
                data.append( vdata_slice[i] )
                data.append( 0.0 )
            vars = [(args[0], 3, 0, data), \
                    ("u_"+args[0], 1, 0, udata_slice ), \
                    ("v_"+args[0], 1, 0, vdata_slice)]
        ncVars = ncVarsU

    else:
        for arg in args:
            for t in xrange(beg_time,end_time):
                if arg in ncVars:
                    data = ncVars[arg][t,kbeg:kend,jbeg:jend,ibeg:iend]
                else:
                    core.sys.exit("ERROR: The variable '"+arg+ \
                        "' is not in the file '"+core.input_filename+"'")
                if isinstance(data, core.np.ma.MaskedArray):
                    # Use the mask to change all masked elements to NaNs
                    data = data.filled( core.np.nan )
                if not isinstance( data, core.np.ndarray ):
                    core.sys.exit( "ERROR: Data is not of type numpy.ndarray" )
                print "data.shape = ", data.shape
                print "data.size = ", data.size
                print "data.ndim = ", data.ndim
                data = data.flatten().tolist()  
                vars.append( (arg,1,0,data) )


    print "lon.shape = ", ncVars["Longitude"][:].shape
    print "lon.size = ", ncVars["Longitude"][:].size
    print "lon.ndim = ", ncVars["Longitude"][:].ndim
    print "lat.shape = ", ncVars["Latitude"][:].shape
    print "lat.size = ", ncVars["Latitude"][:].size
    print "lat.ndim = ", ncVars["Latitude"][:].ndim
    print "depth.shape = ", ncVars["Depth"][:].shape
    print "depth.size = ", ncVars["Depth"][:].size
    print "depth.ndim = ", ncVars["Depth"][:].ndim

    if ncVars["Longitude"][:].ndim == 2:
        print "2 DIMENSIONAL LONGITUDE"
        lon = ncVars["Longitude"][jbeg:jend,ibeg:iend].flatten()
        lon = lon.tolist()*nZ
        print "len(lon) = ", len(lon) 
    else:
        print "1 DIMENSIONAL LONGITUDE"
        lon = ncVars["Longitude"][ibeg:iend].flatten()
        lon = lon.tolist()*nZ*nY
        print "len(lon) = ", len(lon) 

    for i in xrange( len(lon) ):
        lon[i] %= 360

    if ncVars["Latitude"][:].ndim == 2:
        print "2 DIMENSIONAL LATITUDE"
        lat = ncVars["Latitude"][jbeg:jend,ibeg:iend].flatten()
        lat = lat.tolist()*nZ
        print "len(lat) = ", len(lat) 
    else:
        print "1 DIMENSIONAL LATITUDE"
        lat = ncVars["Latitude"][jbeg:jend].flatten()
        lat = lat.tolist()*nZ*nX
        print "len(lat) = ", len(lat) 

    depth = []
    if ncVars["Depth"][:].ndim == 1:
        print "1 DIMENSIONAL DEPTH"
        for d in ncVars["Depth"][kbeg:kend].tolist():
            depth.extend( [d]*nX*nY )
    else:
        core.sys.exit("ERROR: No code to handle multidimensional depths yet")

    vars.append( ("longitude",1,0,lon) )
    vars.append( ("latitude",1,0,lat) )
    print "len(depth) = ", len(depth)
    vars.append( ("depth",1,0,depth) )

    # Check for bathymetry data
    if core.bathymetry != "None":
        if core.os.path.exists(core.bathymetry):
            afile = core.bathymetry
            # replace the .a with .b and save as 'bfile'
            bfile = core.str.replace( core.bathymetry, ".a", ".b" )
            print "afile = ", afile
            print "bfile = ", bfile
            with open( bfile, "r" ) as b:
                with open( afile, "rb" ) as a:
                    lines = b.readlines()
                    # This assumes idm and jdm are always
                    # on lines 7 and 8 respectively
                    idm = int(lines[1].split()[2])
                    jdm = int(lines[1].split()[3])
                    # number of bytes in array
                    n = idm*jdm
                    numbytes = n*4 
                    # each rec is padded to a multiple of 4096
                    pad = (numbytes/4096+1)*4096-numbytes 
                    print "numbytes = ", numbytes
                    print "pad = ", pad
                    end = ">" # Big endian
                    form = "f" # unpack as ieee 32 bit floats
                    #a.read( (lineno-lastRead)*(numbytes+pad) ) # skip through unwanted data
                    print "len(read) = ", len( a.read( numbytes ) )
                    core.sys.exit()
                    bathymetry = core.struct.unpack(end+form*n, a.read( numbytes )) # read data
                    print "len(bathymetry) = ", len(bathymetry)
                    print "type(bathymetry) = ", type(bathymetry)
                    #a.read( pad )
                    filtered = core.filter( lambda x: x<1e30, array ) # remove nans
                    if abs(min(filtered)-float(line[5][3].strip())) > 1e-6:
                        core.sys.exit("ERROR: The data's min is not equal to the .b file's min")
                    if abs(max(filtered)-float(line[5][4].strip())) > 1e-6:
                        core.sys.exit("ERROR: The data's max is not equal to the .b file's max")
        else:
            core.sys.exit("ERROR: Bathymetry file %s does not exist!" % core.bathymetry + \
                    "\nAre you using the full path?")
                    

    # Construct Grid
    conn = []
    pts = []
    nX += 1
    nY += 1
    nZ += 1
    for n in xrange(nX*nY*nZ):
        i = n%nX
        j = (n/nX)%nY
        k = (nZ-1) - n/(nX*nY)
        pts.extend([ i,j,k ])
        if k < nZ-1 and j < nY-1 and i < nX-1:
            pt1 = k*(nX*nY) + j*nX + i;
            pt2 = k*(nX*nY) + j*nX + i+1;
            pt3 = k*(nX*nY) + (j+1)*nX + i+1;
            pt4 = k*(nX*nY) + (j+1)*nX + i;
            pt5 = (k+1)*(nX*nY) + j*nX + i;
            pt6 = (k+1)*(nX*nY) + j*nX + i+1;
            pt7 = (k+1)*(nX*nY) + (j+1)*nX + i+1;
            pt8 = (k+1)*(nX*nY) + (j+1)*nX + i;
            conn.append([ "hexahedron", pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8 ])

    name = core.output_filename

    core.vw.WriteUnstructuredMesh( name, True, pts, conn, vars )
    print "Conversion Complete!"
    print "Output File = ", name
