# core is the base class convert2vtk. It provides access to all the libraries
# and functions included in the class
def convert( core ):

    print "\nConverting "+core.input_filename+" to "+core.output_filename+".vtk..."
    ncVars = core.data.variables
    dimVars = core.data.dimensions
    args = core.variables
    if 'X' in dimVars:
        lenX = len(dimVars['X'])
    elif 'Longitude' in dimVars:
        lenX = len(dimVars['Longitude'])
    elif 'x' in dimVars:
        lenX = len(dimVars['x'])
    else:
        core.sys.exit("ERROR: X-dimension/Longitude variable name not recognized")
    if 'Y' in dimVars:
        lenY = len(dimVars['Y'])
    elif 'Latitude' in dimVars:
        lenY = len(dimVars['Latitude'])
    elif 'y' in dimVars:
        lenY = len(dimVars['y'])
    else:
        core.sys.exit("ERROR: Y-dimension/Latitude variable name not recognized")
    if 'Depth' in dimVars:
        lenZ = len(dimVars['Depth'])
    elif 'Z' in dimVars:
        lenZ = len(dimVars['Z'])
    elif 'z' in dimVars:
        lenZ = len(dimVars['z'])
    elif 'zlevel' in dimVars:
        lenZ = len(dimVars['zlevel'])
    else:
        core.sys.exit("ERROR: Z-dimension/Depth variable name not recognized")
    if 'Time' in dimVars:
        lenT = len(dimVars['Time'])
    elif 'time_counter' in dimVars:
        lenT = len(dimVars['time_counter'])
    elif 'MT' in dimVars:
        lenT = len(dimVars['MT'])
    else:
        core.sys.exit("ERROR: Time variable name not recognized")
    
    # Apply the subsetting
    ibeg, iend, nX, jbeg, jend, nY, kbeg, kend, nZ, tbeg, tend, time = \
    core.subset( lenX, lenY, lenZ, lenT )

    # Make the variables before the grid. This saves the user time if their
    # input values are bad
    vars = []
    for arg in args:
        for t in xrange(tbeg,tend):
            print "\tPacking %s at time %d..." % (arg,t)
            if arg in ncVars:
                data = ncVars[arg][t,kbeg:kend,jbeg:jend,ibeg:iend]
                data[core.np.where( data == -999.0 )] = core.np.nan
                # Subsample the data immediately to speed up future computations
                if core.subsample_num != 'None':
                    data = core.subsample( data )
                if arg == 'u':
                    uFinal = data.flatten().tolist()
                elif arg == 'v':
                    vFinal = data.flatten().tolist()
            else:
                core.sys.exit("\nERROR: The variable '"+arg+ \
                    "' is not in the file '"+core.input_filename+"'")
            if isinstance(data, core.np.ma.MaskedArray):
                # Use the mask to change all masked elements to NaNs
                data = data.filled( core.np.nan )
            if not isinstance( data, core.np.ndarray ):
                core.sys.exit( "\nERROR: Data is not of type numpy.ndarray" )
            data = data.flatten().tolist()  
            vars.append( (arg,1,1,data) )

    if 'u' in args and 'v' in args:
            vec = []
            for i in xrange( len(uFinal) ):
                vec.append( uFinal[i] )
                vec.append( vFinal[i] )
                if uFinal[i] == core.np.nan and vFinal[i] == core.np.nan:
                    vec.append( core.np.nan )
                else:
                    vec.append( 0.0 )
            vars.append( ("uv",3,1,vec) )

    if ncVars["elon"][:].ndim == 2:
        nplon = ncVars["elon"][jbeg:jend,ibeg:iend]
        # This is for lon coordinates around the poles, it puts them all between 0 and 360
        nplon %= 360
        # Subsample the data immediately to speed up future computations
        if core.subsample_num != 'None':
            nplon = core.subsample( nplon )
        lon = nplon.flatten().tolist()*nZ
    else:
        nplon = ncVars["elon"][ibeg:iend]
        # This is for lon coordinates around the poles, it puts them all between 0 and 360
        nplon %= 360
        # Subsample the data immediately to speed up future computations
        if core.subsample_num != 'None':
            nplon = core.subsample( nplon[ibeg:iend] )
        lon = nplon.flatten().tolist()*nZ*nY

    if ncVars["alat"][:].ndim == 2:
        nplat = ncVars["alat"][jbeg:jend,ibeg:iend]
        # Subsample the data immediately to speed up future computations
        if core.subsample_num != 'None':
            nplat = core.subsample( nplat )
        lat = nplat.flatten().tolist()*nZ
    else:
        nplat = ncVars["alat"][jbeg:jend]
        # Subsample the data immediately to speed up future computations
        if core.subsample_num != 'None':
            nplat = core.subsample( nplat )
        lat = nplat.flatten().tolist()*nZ*nX

    # There are problems saving these along with the other varibles
    vars.append( ("longitude",1,1,lon) )
    vars.append( ("latitude",1,1,lat) )

    name = core.output_filename
    bathName = name+"_bathymetry"

    # Check if bathymetry has already been created
    if core.os.path.exists( bathName+".vtk" ):
        BATH_FLAG = False
    else:
        BATH_FLAG = True
        

    #-------------- Curvilinear MESH ---------------------
    if BATH_FLAG:
        print "\tGenerating Curvilinear Mesh and Bathymetry..."
    else:
        print "\tGenerating Curvilinear Mesh..."

    # Add one to indices because this is used for the mesh and the data is cell centered
    # (Fence post problem)
    bathData = ncVars["h"][jbeg:jend,ibeg:iend]
    # Subsample the data immediately to speed up future computations
    if core.subsample_num != 'None':
        bathData = core.subsample( bathData )

    # Make bathymetry variable, h
    h = core.np.zeros( (4,nY,nX) )
    h[2:] = 1
    h = h.flatten().tolist()
    bathVars = [ ("h",1,1,h) ]

    depth = ncVars["z"][kbeg:kend,jbeg:jend,ibeg:iend]
    # Subsample the data immediately to speed up future computations
    if core.subsample_num != 'None':
        depth = core.subsample( depth )

    for i,layer in enumerate(depth[:]):
        if i == 0:
            max = core.np.max( layer[ core.np.where( layer <= 0 ) ] )
        else:
            max = core.np.max( layer[ core.np.where( layer < 0 ) ] )
        layer[core.np.where( layer == 999 )] = max


    pts = []
    bathPts = []
    if ncVars["elon"][:].ndim == 2 and ncVars["alat"][:].ndim == 2:
        last_n = 0
        for n in xrange(nX*nY*nZ):
            i = n%nX
            j = (n/nX)%nY
            k = n/(nX*nY)
            if core.gridspace:
                x = ibeg+i
                y = jbeg+j
            else:
                x = float(nplon[j,i])
                y = float(nplat[j,i])
            z = float(depth[k,j,i])
            pts.extend([ x,y,z ])
            if k < 4 and BATH_FLAG:
                if k == 0:
                    z = float(depth[0,j,i])
                elif k == 1:
                    z = float(bathData[j,i])+.00001
                elif k == 2:
                    z = float(bathData[j,i])-.00001
                elif k == 3:
                    z = float(depth[-1,j,i])

                bathPts.extend( [x,y,z] )
            last_n = n
            if nZ < 4:
                for n in xrange( last_n+1,nX*nY*4 ): 
                    i = n%nX
                    j = (n/nX)%nY
                    k = n/(nX*nY)
                    if k == 0:
                        z = depth[0,j,i]
                    elif k == 1:
                        z = float(bathData[j,i])+.01
                    elif k == 2:
                        z = float(bathData[j,i])-.01
                    elif k == 3:
                        z = depth[-1,j,i]

                    bathPts.extend( [x,y,z] )


    dims = [nX,nY,nZ]
    core.vw.WriteCurvilinearMesh( name, True, dims, pts, vars )
    if BATH_FLAG:
        bathDims = [nX,nY,4]
        core.vw.WriteCurvilinearMesh( bathName, True, bathDims, bathPts, bathVars )
        print "\nBoth the bathymetry\n\t", bathName, "\nand data file\n\t", name, "\nhave been created.\n"
    else:
        print "\nThe data file\n\t", name, "\nhas been created.\n"
