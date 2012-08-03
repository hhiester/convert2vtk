def load_mesh( core, filename ):
    """ If the file you wish to convert doesn't have any mesh data in it
        use this routine to load a mesh from another NetCDF file """
    print "In the load_mesh routine"

    # Check to see if the file is a NetCDF file
    if filename[-3:] == ".nc":
        # If so, try to open it using the NetCDF library
        try:
            core.mesh = core.nc.Dataset( filename, 'r' )
        except:
            sys.exit( "\nERROR: Failed to open the netcdf file \
\n\n\t%s\n\nAre you using the full path?\n" % filename )

    else:
        sys.exit( "The mesh input file %s is not a NetCDF file" % filename )


def convert( core ):
    print "Converting dmitry's files to vtk..."

<<<<<<< HEAD
    meshData = "/panfs/storage.local/coaps/home/ddmitry/fvcom/fvcom/models/ike/outputT03/ike_0040.nc"
    load_mesh( core, meshData )
=======
    meshData = "/panfs/storage.local/coaps/home/ndc08/code/hycom_data/ike_0024.nc"
    load_mesh( core, meshData)
>>>>>>> eb0cbca65dcd113bc12fd557fb46327e4756b1ae
    meshVars = core.mesh.variables
    dataVars = core.data.variables

    # Extract the dimensions and time for future use
    numberOfElements = len(core.mesh.dimensions['nele'])
    numberOfNodes = len(core.mesh.dimensions['node'])
    totalTime = len(core.mesh.dimensions['time'])
    print "time = ", core.mesh.dimensions['time']
    if totalTime == None or totalTime == "UNLIMITED":
        totalTime = 45
    totalTime = 45

    node_x = meshVars['x'][:].tolist()
    node_y = meshVars['y'][:].tolist()

    # Node coordinates
    pts = []
    for i in xrange( numberOfNodes ):
        try:
            pts.append( node_x[i] )  
            pts.append( node_y[i] )  
            pts.append( 0.0 ) 
        except IndexError as ie:
            print "IndexError: ", ie 
            sys.exit( "index i = %d" % i )
        except:
            sys.exit( "Error occured creating pts" )

    # Connectivity
    parts = meshVars['nv'][:].tolist()
    conn = []
<<<<<<< HEAD
    #print "parts[0][0] = ", parts[0][0]
    #print "parts[1][0] = ", parts[0][0]
    #print "parts[2][0] = ", parts[0][0]
=======
>>>>>>> eb0cbca65dcd113bc12fd557fb46327e4756b1ae
    for i in xrange( numberOfElements ):
        conn.append( ("triangle", parts[0][i]-1, parts[1][i]-1, parts[2][i]-1 ) )

    print "totalTime = ", totalTime
    for time in xrange( totalTime ):
        # Data arrays
        u_wind = dataVars['uwind_stress'][:][time].tolist()
        v_wind = dataVars['vwind_stress'][:][time].tolist()
<<<<<<< HEAD
        #print "u_wind[0] = ", u_wind[0] 
        #print "v_wind[0] = ", v_wind[0] 
        wind = []
        for i in xrange( numberOfElements ):
            try:
                wind.append( u_wind[i] )
                wind.append( v_wind[i] )
                wind.append( 0.0 )
            except:
                print "SHIT GUYS, i = ", i
=======
        wind = []
        for i in xrange( numberOfElements ):
            wind.append( u_wind[i] )
            wind.append( v_wind[i] )
            wind.append( 0.0 )
>>>>>>> eb0cbca65dcd113bc12fd557fb46327e4756b1ae

        # Create the variables such as vectors (velocity) and scalars (temperature/salinity)
        vars = [("wind", 3, 0, wind), ("u_wind", 1, 0, u_wind ), ("v_wind", 1, 0, v_wind)]

        # Pass the data to visit_writer
        name = core.output_filename+"%02d"%time
        print "output_filename = ", name
        core.vw.WriteUnstructuredMesh( name, True, pts, conn, vars)
