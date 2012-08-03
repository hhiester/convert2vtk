# Used to transform the s depths back to world coordinates (meters)
def set_depth( core, z, Vtransform, Vstretching, theta_s, theta_b, hc, N, h, zeta ):

    s,C = stretching( core, Vstretching, theta_s, theta_b, hc, N )

    if Vtransform == 1:
        for k in xrange(N):
            z0 = (s[k]-C[k])*hc + C[k]*h
            z[k,:,:] = z0 + zeta*(1.0 + z0/h)
    elif Vtransform == 2:
        for k in xrange(N):
            z0 = (hc*s[k]+C[k]*h)/(hc+h)
            z[k,:,:] = zeta+(zeta+h)*z0


# Used to transform the s depths back to world coordinates (meters)
def stretching( core, Vstretching, theta_s, theta_b, hc, N ):

    if Vstretching == 1:
        ds = 1.0/N

        Nlev = N
        lev = core.np.arange(N)-0.5
        s = (lev-N)*ds
        if theta_s > 0:
            Ptheta = core.np.sinh(theta_s*s)/core.np.sinh(theta_s)
            Rtheta = core.np.tanh(theta_s*(s+0.5))/(2.0*core.np.tanh(0.5*theta_s))-0.5
            C = (1.0-theta_b)*Ptheta+theta_b*Rtheta
        else:
            C=s

    elif Vstretching == 2:

        alfa = 1.0
        beta = 1.0
        ds = 1.0/N
        Nlev = N
        lev = np.arange(N)-0.5
        s = (lev-N)*ds
        if theta_s > 0:
            Csur = (1.0-core.np.cosh(theta_s*s))/(core.np.cosh(theta_s)-1.0)
            if theta_b > 0:
                Cbot = -1.0+core.np.sinh(theta_b*(s+1.0))/core.np.sinh(theta_b)
                weigth = (s+1.0)^alfa*(1.0+(alfa/beta)*(1.0-(s+1.0)^beta))
                C = weigth*Csur+(1.0-weigth)*Cbot
            else:
                C = Csur
        else:
            C = s

    elif Vstretching == 3:

        ds = 1.0/N
        Nlev = N
        lev = np.arage(N)-0.5
        s = (lev-N)*ds
        if theta_s > 0:
            exp_s = theta_s
            exp_b = theta_b
            alpha = 3     
            Cbot = core.np.log(core.np.cosh(alpha*(s+1)^core.np.exp(b)))/core.np.log(core.np.cosh(alpha))-1
            Csur = -core.np.log(core.np.cosh(alpha*core.np.abs(s)^core.np.exp(s)))/core.np.log(core.np.cosh(alpha))
            weight = (1-core.np.tanh( alpha*(s+.5)))/2
            C = weight*Cbot+(1-weight)*Csur
        else:
            C = s

    elif Vstretching == 4:
        ds = 1.0/N
        Nlev = N
        lev = core.np.arange(N)-0.5
        s = (lev-N)*ds
        if theta_s > 0:
            Csur = (1.0-core.np.cosh(theta_s*s))/(core.np.cosh(theta_s)-1.0)
        else:
            Csur = -s^2
        if theta_b > 0:
            Cbot = (core.np.exp(theta_b*Csur)-1.0)/(1.0-core.np.exp(-theta_b))
            C = Cbot
        else:
            C = Csur

    return s,C


# core is the base class convert2vtk. It provides access to all the libraries
# and functions included in the class
def convert( core ):

    print "\nConverting "+core.input_filename+" to "+core.output_filename+".vtk..."
    ncVars = core.data.variables
    dimVars = core.data.dimensions
    args = core.variables
    if 'xi_rho' in dimVars:
        lenX = len(dimVars['xi_rho'])
    else:
        core.sys.exit("ERROR: X-dimension/Longitude variable name not recognized")
    if 'eta_rho' in dimVars:
        lenY = len(dimVars['eta_rho'])
    else:
        core.sys.exit("ERROR: Y-dimension/Latitude variable name not recognized")
    if 's_rho' in dimVars:
        lenZ = len(dimVars['s_rho'])
    else:
        core.sys.exit("ERROR: Z-dimension/Depth variable name not recognized")
    if 'ocean_time' in dimVars:
        lenT = len(dimVars['ocean_time'])
    else:
        core.sys.exit("ERROR: Time variable name not recognized")

    # Apply the subsetting
    ibeg, iend, nX, jbeg, jend, nY, kbeg, kend, nZ, tbeg, tend, time = \
    core.subset( lenX, lenY, lenZ, lenT )

    # Make the variables before the grid. This saves the user time if their
    # input values are bad
    vars = []
    for t in xrange(tbeg,tend):
        for arg in args:
            print "\tPacking %s at time %d..." % (arg,t)
            if arg in ncVars:
                if arg == 'u':
                    udata = ncVars[arg][t,kbeg:kend,jbeg:jend,ibeg:iend]
                    umask = ncVars['mask_u'][jbeg:jend,ibeg:iend-1]
                    indices = core.np.where( umask == 0 )
                    for layer in udata[:]:
                        layer[indices] = core.np.nan
                    zsz,ysz,xsz = udata.shape
                    data = core.np.ndarray( (zsz, ysz, xsz+1) ) 
                    data[:,:,:-1] = udata
                    data[:,:,-1] = data[:,:,-2]+(data[:,:,-2]-data[:,:,-3])
                    # Subsample the data immediately to speed up future computations
                    if core.subsample_num != 'None':
                        data = core.subsample( data )
                    uFinal = data.flatten().tolist()
                elif arg == 'v':
                    vdata = ncVars[arg][t,kbeg:kend,jbeg:jend,ibeg:iend]
                    vmask = ncVars['mask_v'][jbeg:jend-1,ibeg:iend]
                    indices = core.np.where( vmask == 0 )
                    for layer in vdata[:]:
                        layer[indices] = core.np.nan
                    zsz,ysz,xsz = vdata.shape
                    data = core.np.ndarray( (zsz, ysz+1, xsz) ) 
                    data[:,:-1,:] = vdata
                    data[:,-1,:] = data[:,-2,:]+(data[:,-2,:]-data[:,-3,:])
                    # Subsample the data immediately to speed up future computations
                    if core.subsample_num != 'None':
                        data = core.subsample( data )
                    vFinal = data.flatten().tolist()
                else:
                    data = ncVars[arg][t,kbeg:kend,jbeg:jend,ibeg:iend]
                    rmask = ncVars['mask_rho'][jbeg:jend,ibeg:iend]
                    indices = core.np.where( rmask == 0 )
                    for layer in data[:]:
                        layer[indices] = core.np.nan
                    # Subsample the data immediately to speed up future computations
                    if core.subsample_num != 'None':
                        data = core.subsample( data )
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

        if ncVars["lon_rho"][:].ndim == 2:
            nplon = ncVars["lon_rho"][jbeg:jend,ibeg:iend]
            if core.subsample_num != 'None':
                nplon = core.subsample( nplon )
            # This is for lon coordinates around the poles, it puts them all between 0 and 360
            nplon %= 360
            lon = nplon[jbeg:jend,ibeg:iend].flatten().tolist()*nZ
        else:
            nplon = ncVars["lon_rho"][ibeg:iend]
            if core.subsample_num != 'None':
                nplon = core.subsample( nplon )
            # This is for lon coordinates around the poles, it puts them all between 0 and 360
            nplon %= 360
            lon = nplon[ibeg:iend].flatten().tolist()*nZ*nY

        if ncVars["lat_rho"][:].ndim == 2:
            nplat = ncVars["lat_rho"][jbeg:jend,ibeg:iend]
            if core.subsample_num != 'None':
                nplat = core.subsample( nplat )
            lat = nplat[jbeg:jend,ibeg:iend].flatten().tolist()*nZ
        else:
            nplat = ncVars["lat_rho"][jbeg:jend]
            lat = nplat[jbeg:jend].flatten().tolist()*nZ*nX

        vars.append( ("longitude",1,1,lon) )
        vars.append( ("latitude",1,1,lat) )


        #-------------- Curvilinear MESH ---------------------
        name = core.output_filename
        directory = "/".join( name.split("/")[:-1] )
        print "name = ", name
        print "directory = ", directory
        bathName = directory+"/bathymetry"

        # Check if bathymetry has already been created
        if core.os.path.exists( bathName+".vtk" ):
            BATH_FLAG = False
        else:
            BATH_FLAG = True
 
        if BATH_FLAG:
            print "\tGenerating Curvilinear Mesh and Bathymetry..."
        else:
            print "\tGenerating Curvilinear Mesh..."
           

        bathData = ncVars['h'][jbeg:jend,ibeg:iend]
        if core.subsample_num != 'None':
            bathData = core.subsample( bathData )

        # Make bathymetry variable, h
        h = core.np.zeros( (4,nY,nX) )
        h[2:] = 1
        h = h.flatten().tolist()
        bathVars = [ ("h",1,1,h) ]

        # Variables for transforming the s coordinates back to actual depth
        Vtrans = int(ncVars['Vtransform'][:][0])
        Vstretch = int(ncVars['Vstretching'][:][0])
        theta_s = float(ncVars['theta_s'][:][0])
        theta_b = float(ncVars['theta_b'][:][0])
        hc = float(ncVars['hc'][:][0])
        zeta = ncVars['zeta'][t][jbeg:jend,ibeg:iend]
        if core.subsample_num != 'None':
            zeta = core.subsample( zeta )
        depth = core.np.zeros( (nZ,nY,nX) )
         
        # Calculate the actual depths
        set_depth( core, depth, Vtrans, Vstretch, theta_s, theta_b, hc, nZ, bathData, zeta )
        # Now convert the rmask to be of same dimension as everything else  
        if core.subsample_num != 'None':
            rmask = core.subsample( rmask )

        # set_depth requires the bathymetry to be positive, so the values must
        # be switched here, after the conversion
        bathData = -bathData

  
        # Mask the depth data
        indices = core.np.where( rmask == 0 )
        for i,layer in enumerate(depth[:]):
            if i == 0:
                max = core.np.max( layer[ core.np.where( layer <= 0 ) ] )
            else:
                max = core.np.max( layer[ core.np.where( layer < 0 ) ] )
            layer[indices] = max
      
        pts = []
        bathPts = []
        if ncVars["lon_rho"][:].ndim == 2 and ncVars["lat_rho"][:].ndim == 2:
            last_n = 0
            for n in xrange(nX*nY*nZ):
                i = n%nX
                j = (n/nX)%nY
                k = n/(nX*nY)
                if core.gridspace:
                    x = ibeg+i
                    y = jbeg+j
                else:
                    x = nplon[j,i]
                    y = nplat[j,i]
                z = depth[k,j,i]
                pts.extend([ x,y,z ])
                if k < 4 and BATH_FLAG:
                    if k == 0:
                        z = depth[0,j,i]
                    elif k == 1:
                        z = float(bathData[j,i])+.00001
                    elif k == 2:
                        z = float(bathData[j,i])-.00001
                    elif k == 3:
                        z = depth[-1,j,i]
                        
                    bathPts.extend( [x,y,z] )
                last_n = n
            if nZ < 4:
                for n in xrange( last_n+1,nX*nY*4 ): 
                    i = n%nX
                    j = (n/nX)%nY
                    k = n/(nX*nY)
                    if core.gridspace:
                        x = ibeg+i
                        y = jbeg+j
                    else:
                        x = nplon[j,i]
                        y = nplat[j,i]
                    if k == 0:
                        z = depth[0,j,i]
                    elif k == 1:
                        z = float(bathData[j,i])+.00001
                    elif k == 2:
                        z = float(bathData[j,i])-.00001
                    elif k == 3:
                        z = depth[-1,j,i]

                    bathPts.extend( [x,y,z] )

        dims = [nX,nY,nZ]
        core.vw.WriteCurvilinearMesh( name, True, dims, pts, vars )
        if BATH_FLAG:
            bathDims = [nX,nY,4]
            print "bathname = ", bathName
            print "bathDims = ", bathDims
            print "len(bathPts)/3 = ", len(bathPts)/3.0
            print "len(h) = ", len(h)
            print "max(bathPts) = ", core.np.max(bathPts)
            print "min(bathPts) = ", core.np.min(bathPts)
            print "max(depth) = ", core.np.max(depth)
            print "min(depth) = ", core.np.min(depth)
            core.vw.WriteCurvilinearMesh( bathName, True, bathDims, bathPts, bathVars )


