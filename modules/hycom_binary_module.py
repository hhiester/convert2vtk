

def convert( core ):
    """ convert the loaded binary hycom files into vtk files """
    print "In the hycom_binary.convert routine"

    args = core.variables
    print "arg list = ", args

    afile = core.data
    # replace the .a with .b and save as 'bfile'
    bfile = str.replace( core.data, ".a", ".b" )
    with open( bfile, "r" ) as b:
        with open( afile, "rb" ) as a:
            lines = b.readlines()
            # This assumes idm and jdm are always
            # on lines 7 and 8 respectively
            idm = int(lines[7].split()[0])
            jdm = int(lines[8].split()[0])
            # read the last k value
            kdm = int(lines[-1].split()[4])
            # number of bytes in array
            n = idm*jdm
            numbytes = n*4 
            # each rec is padded to a multiple of 4096
            pad = (numbytes/4096+1)*4096-numbytes 
            print "numbytes = ", numbytes
            print "pad = ", pad
            end = ">" # Big endian
            form = "f" # unpack as ieee 32 bit floats
            vars = {} # store all the variables in a dictionary of lists
            lastRead = 0
            for lineno,line in enumerate( lines[10:] ):
                line = line.split()
                varName = line[0].strip()
                print "varName = ", varName
                if varName in args:
                    print varName, "is in args!"
                    print "lineno = ", lineno
                    print "lastRead = ", lastRead
                    a.read( (lineno-lastRead)*(numbytes+pad) ) # skip through unwanted data
                    array = core.struct.unpack(end+form*n, a.read( numbytes )) # read data
                    a.read( pad )
                    lastRead = lineno+1 # save the last line read for skipping future lines
                    if varName in vars:
                        # Append this array to the list of arrays (this makes it easier to
                        # convert all the arrays into a 3 dimensional list later on)
                        print varName, " is in vars!"

                        # Do some preliinary error checking
                        filtered = filter( lambda x: x<1e30, array ) # remove nans
                        if abs(min(filtered)-float(line[6].strip())) > 1e-6:
                            sys.exit("ERROR: The data's min is not equal to the .b file's min")
                        if abs(max(filtered)-float(line[7].strip())) > 1e-6:
                            sys.exit("ERROR: The data's max is not equal to the .b file's max")
                        if len(vars[varName])+1 != int( line[4].strip() ):
                            sys.exit("ERROR: Level of this array is out of sequence. Missed a record")
                        
                        vars[varName].append( core.np.array( array ) )

                    else:
                        # Else add a new element to the dictionary
                        print "Adding new element ", varName, " to vars!"
                        vars[varName] = [ core.np.array( array ) ]
            
            print "vars.keys()[1] = ", vars.keys()
            print "len( vars.values()[1] ) = ", len(vars.values()[1])

    # Convert to vtk now  
    # Make mesh...
            
    nX = idm
    nY = jdm
    nZ = kdm 
    conn = []
    pts = []
    rad = []
    cntr = 0
    for k in range(nZ):
        for j in range(nY):
            for i in range(nX):
                #print "pt%d = (%d,%d,%d)" % (cntr,i,j,k)
                cntr += 1
                pts.extend([ i, j, k ])
                rad.append( 0 )
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
                
#        variables = []
#        for name,lst in vars.iteritems():
#            fullArray = core.np.ndarray( (kdm,jdm,idm) )
#            print "fullArray.shape = ", fullArray.shape
#            print "fullArray[0].shape = ", fullArray[0].shape
#            print "fullArray[:].shape = ", fullArray[:].shape
#            print "fullArray[:][0].shape = ", fullArray[:][0].shape
#            print "fullArray[:][:][0].shape = ", fullArray[:][:][0].shape
#            print "fullArray.ndim = ", fullArray.ndim
#            print "fullArray.size = ", fullArray.size
#            for lvl,array in enumerate(lst):
#                print "Level = ", lvl
#                print "array.shape = ", array.shape
#                print "array.ndim = ", array.ndim
#                print "array.size = ", array.size
#                tmp = array.reshape( jdm,idm )
#                print "tmp.shape = ", tmp.shape
#                print "tmp.ndim = ", tmp.ndim
#                print "tmp.size = ", tmp.size
#                fullArray[lvl] = array.reshape( jdm,idm )
#            variables.append( (name, 1, 1, fullArray.tolist()) )

##
#        for time in xrange( totalTime ):
#            # Data arrays
#            u_wind = dataVars['uwind_stress'][:][time].tolist()
#            v_wind = dataVars['vwind_stress'][:][time].tolist()
#            wind = []
#            for i in xrange( numberOfElements ):
#                wind.append( u_wind[i] )
#                wind.append( v_wind[i] )
#                wind.append( 0.0 )
#
#            # Create the variables such as vectors (velocity) and scalars (temperature/salinity)
#            vars = [("wind", 3, 0, wind), ("u_wind", 1, 0, u_wind ), ("v_wind", 1, 0, v_wind)]
##
           
    variables = core.np.zeros( len(pts) )
    print "variables.shape = ", variables.shape
    print "variables.ndim = ", variables.ndim
    print "variables.size = ", variables.size

    print "len(pts) = ", len(pts)
    print "len(pts)/3 = ", len(pts)/3
    
    var_datum = [ "radius", 1, 1, variables.tolist() ]
    vars = [ var_datum ]
    outfile = core.output + ".vtk"
    core.vw.WriteUnstructuredMesh(outfile, 0, pts, conn, vars)


