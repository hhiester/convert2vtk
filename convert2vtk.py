import sys
import os

# Path to libs
sys.path.append("/panfs/storage.local/coaps/home/ndc08/code/converter/libs/lib64")
# Path to modules
sys.path.append("/panfs/storage.local/coaps/home/ndc08/code/converter/modules")

class convert2vtk():
    """ Read in a model's output data file

            Currently supports:
                HYCOM Binary (Incomplete)
                HYCOM Z Level
                NCOM
                HYCOM Binary (Not Implemented Yet)
                HYCOM Z Level
                NCOM (Not Implemented Yet)
                ROMS (Not Implemented Yet)

        and convert it into a vtk file for easy visualization in VisIt\n """
    
    import sys
    import os
    import numpy as np
    import visit_writer as vw
    import netCDF4 as nc
    import string as str
    import struct
    import resource

    # Set stack memory limit to maximum 
    resource.setrlimit( resource.RLIMIT_STACK, (-1,-1) )

    def __init__( self, init_vars ):
        """ Initialization Routine - Create the output folder to hold the vtk files 
        init_vars - dictionary of initialization variables"""
        #print "In the __init__ routine"
        print "In the __init__ routine"

        self.filetype = init_vars['input_filetype']
        self.input_filename = init_vars['input_filename']
        self.input_filename_u = init_vars['filename_u']
        self.input_filename_v = init_vars['filename_v']
        self.output_directory = init_vars['output_directory']
        self.output_filename = init_vars['output_filename']
        self.variables = init_vars['variables']
        self.ibegin = init_vars['ibegin']
        self.iend = init_vars['iend']
        self.jbegin = init_vars['jbegin']
        self.jend = init_vars['jend']
        self.kbegin = init_vars['kbegin']
        self.kend = init_vars['kend']
        self.time_begin = init_vars['time_begin']
        self.time_end = init_vars['time_end']
        self.vector = init_vars['vector']
        self.bathymetry = init_vars['bathymetry']
        self.gridspace = init_vars['gridspace']
        self.subsample_num = init_vars['subsample']
        self.datau = None
        self.datav = None
        self.time_end = init_vars['time_end']
        self.vector = init_vars['vector']
        self.bathymetry = init_vars['bathymetry']
        if self.vector == "True":
            self.vector == True
            self.datau = None
            self.datav = None
        else:
            self.vector == False
            self.data = None
            self.mesh = None

        if not os.path.exists( self.output_directory ):
            os.makedirs( self.output_directory )

        self.__load()
        return


    def __del__( self ):
        """ Destructor - Nothing needed yet """
        #print "In the __del__ routine"
        print "In the __del__ routine"

        return


    def __load( self ):
        """ Load the initialization variables into memory for conversion. """ 
        #print "In the load routine"

    # ---------------------------------- Hycom Z level files ------------------------------
        print "In the load routine"

# ---------------------------------- Hycom Z level files ------------------------------

        if self.filetype == "hycom_z":
            if self.vector == True:

                # If so, try to open them using the NetCDF library
                try:
                    self.datau = self.nc.Dataset( self.input_filename_u, 'r' )
                except:
                    sys.exit( "\nERROR: Failed to open the hycom file \n\n\t"+ \
                            "%s\n\nAre you using the full path?\n" % self.input_filename_u )
                self.filetype = "hycom_z"
                try:
                    self.datav = self.nc.Dataset( self.input_filename_v, 'r' )
                except:
                    sys.exit( "\nERROR: Failed to open the hycom file \n\n\t"+ \
                            "%s\n\nAre you using the full path?\n" % self.input_filename_v )
                if self.filetype == "dmitry":
                    sys.exit("A Dmitry file type with vector variables?? Double check this")
                self.filetype = "hycom_z"

                # Grab only the name of the file for output, if it is in a full path
                if self.output_filename == 'None':
                    if self.output_directory[-1] == "/":
                        self.output_filename = self.output_directory+ \
                                            self.input_filename.split("/")[-1][:-3]
                    else:
                        self.output_filename = self.output_directory+"/"+ \
                                            self.input_filename.split("/")[-1][:-3]
                elif self.output_directory[-1] == "/":
                    self.output_filename = self.output_directory+self.output_filename
                else:
                    self.output_filename = self.output_directory+"/"+self.output_filename
                print "The files read in were ", self.filetype, "files."
            else:
                try:
                    self.data = self.nc.Dataset( self.input_filename, 'r' )
                except:
                    sys.exit( "\nERROR: Failed to open the hycom file \n\n\t"+ \
                            "%s\n\nAre you using the full path?\n" % self.input_filename )
                if self.filetype != "dmitry":
                    self.filetype = "hycom_z"
                if self.output_filename == 'None':
                    # Grab only the name of the file for output, if it is in a full path
                    if self.output_directory[-1] == "/":
                        self.output_filename = self.output_directory+ \
                                            self.input_filename.split("/")[-1][:-3]
                    else:
                        self.output_filename = self.output_directory+"/"+ \
                                            self.input_filename.split("/")[-1][:-3]
                elif self.output_directory[-1] == "/":
                    self.output_filename = self.output_directory+self.output_filename
                else:
                    self.output_filename = self.output_directory+"/"+self.output_filename

    # ---------------------------------- Hycom files --------------------------------------
                print "The file read in \n\n", self.input_filename.split("/")[-1], \
                        "is a", self.filetype, "file."

# ---------------------------------- Hycom files --------------------------------------

        elif self.input_filename[-2:] == ".a" and self.filetype == "hycom_binary":
            # Only store the filename in memory for now
            self.data = self.input_filename
            self.filetype = "hycom_binary"
            # Grab only the name of the file for output, if it is in a full path
            if self.output+filename == 'None':
                self.output_filename = self.output_directory+"/"+ \
                                    self.input_filename.split("/")[-1][:-2]


    # ---------------------------------- Ncom files --------------------------------------

        elif self.filetype == "ncom":
            try:
                self.data = self.nc.Dataset( self.input_filename, 'r' )
            except:
                sys.exit( "\nERROR: Failed to open the ncom file \n\n\t"+ \
                        "%s\n\nAre you using the full path?\n" % self.input_filename )
            if self.output_filename == 'None':
                # Grab only the name of the file for output, if it is in a full path
                if self.output_directory[-1] == "/":
                    self.output_filename = self.output_directory+ \
                                        self.input_filename.split("/")[-1][:-3]
                else:
                    self.output_filename = self.output_directory+"/"+ \
                                        self.input_filename.split("/")[-1][:-3]
            elif self.output_directory[-1] == "/":
                self.output_filename = self.output_directory+self.output_filename
            else:
                self.output_filename = self.output_directory+"/"+self.output_filename


    # ---------------------------------- Roms files --------------------------------------

        elif self.filetype == "roms":
            try:
                self.data = self.nc.Dataset( self.input_filename, 'r' )
            except:
                sys.exit( "\nERROR: Failed to open the roms file \n\n\t"+ \
                        "%s\n\nAre you using the full path?\n" % self.input_filename )
            if self.output_filename == 'None':
                # Grab only the name of the file for output, if it is in a full path
                if self.output_directory[-1] == "/":
                    self.output_filename = self.output_directory+ \
                                        self.input_filename.split("/")[-1][:-3]
                else:
                    self.output_filename = self.output_directory+"/"+ \
                                        self.input_filename.split("/")[-1][:-3]
            elif self.output_directory[-1] == "/":
                self.output_filename = self.output_directory+self.output_filename
            else:
                self.output_filename = self.output_directory+"/"+self.output_filename

    # ---------------------------------- Dmitry's files --------------------------------------

        elif self.filetype == "dmitry":
            try:
                self.data = self.nc.Dataset( self.input_filename, 'r' )
            except:
                sys.exit( "\nERROR: Sorry Dmitry, I failed to open your file \n\n\t"+ \
                        "%s\n\nAre you using the full path?\n" % self.input_filename )
            if self.output_filename == 'None':
                # Grab only the name of the file for output, if it is in a full path
                if self.output_directory[-1] == "/":
                    self.output_filename = self.output_directory+ \
                                        self.input_filename.split("/")[-1][:-3]
                else:
                    self.output_filename = self.output_directory+"/"+ \
                                        self.input_filename.split("/")[-1][:-3]
            elif self.output_directory[-1] == "/":
                self.output_filename = self.output_directory+self.output_filename
            else:
                self.output_filename = self.output_directory+"/"+self.output_filename


    # ---------------------------------- Unrecognized files -------------------------------
            print "The file read in \n\n", self.input_filename.split("/")[-1], \
                    "is a", self.filetype, "file."

# ---------------------------------- Unrecognized files -------------------------------

        else:
            sys.exit( "\nERROR: The filetype to be converted \n\n%s\n\n" % self.input_filename+ \
                    "is not recognized!\n")
 
       

    def convert( self ):
        """ Convert the input file(s) into vtk file(s) """
        #print "In the convert routine"
        print "In the convert routine"

        if self.filetype == "hycom_binary":
            self.__convertHycomB()
        elif self.filetype == "hycom_z":
            self.__convertHycomZ()
        elif self.filetype == "ncom":
            self.__convertNcom()
        elif self.filetype == "roms":
            self.__convertRoms()
            pass
        elif self.filetype == "roms":
            pass
        elif self.filetype == "dmitry":
            self.__convertDmitry()


    def __convertHycomB( self ):
        import hycom_binary_module as hycom_binary
        hycom_binary.convert( self )


    def __convertHycomZ( self ):
        import hycom_z_module as hycom_z
        hycom_z.convert( self )


    def __convertDmitry( self ):
        import dmitry_module as dmitry
        dmitry.convert( self )


    def __convertNcom( self ):
        import ncom_module as ncom
        ncom.convert( self )


    def __convertRoms( self ):
        import roms_module as roms
        roms.convert( self )

    def subset( self, lenX, lenY, lenZ, lenT ):

        # Set up the x slicing range
        if (self.ibegin == 'None' and self.iend == 'None') \
            or (self.ibegin == 'None' and self.iend == lenX) \
            or (self.ibegin == 0 and self.iend == 'None') \
            or (self.ibegin == 0 and self.iend == lenX):
            ibeg = 0
            iend = lenX
            nX = iend
        elif (self.ibegin == 'None' and self.iend != 'None') \
            or (self.ibegin == 0 and self.iend != 'None'):
            ibeg = 0
            iend = int(self.iend)+1
            nX = iend
        elif (self.iend == 'None' and self.ibegin != 'None') \
            or (self.iend == 0 and self.ibegin != 'None'):
            ibeg = int(self.ibegin)
            iend = lenX
            nX = iend-ibeg
        elif self.iend == self.ibegin:
            ibeg = int(self.ibegin)
            iend = int(self.iend)+1
            nX = 1
        else:
            if self.iend > self.ibegin:
                ibeg = int(self.ibegin)
                iend = int(self.iend)+1
                nX = iend-ibeg
            else:
                self.sys.exit("Ending i slice %d must be greater than begining i slice %d" % (self.iend,self.ibegin))


        # Set up the y slicing range
        if (self.jbegin == 'None' and self.jend == 'None') \
            or (self.jbegin == 'None' and self.jend == lenY) \
            or (self.jbegin == 0 and self.jend == 'None') \
            or (self.jbegin == 0 and self.jend == lenY):
            jbeg = 0
            jend = lenY
            nY = jend
        elif (self.jbegin == 'None' and self.jend != 'None') \
            or (self.jbegin == 0 and self.jend != 'None'):
            jbeg = 0
            jend = int(self.jend)+1
            nY = jend
        elif (self.jend == 'None' and self.jbegin != 'None') \
            or (self.jend == 0 and self.jbegin != 'None'):
            jbeg = int(self.jbegin)
            jend = lenY
            nY = jend-jbeg
        elif self.jend == self.jbegin:
            jbeg = int(self.jbegin)
            jend = int(self.jend)+1
            nY = 1
        else:
            jbeg = int(self.jbegin)
            jend = int(self.jend)+1
            nY = jend-jbeg


        # Set up the z slicing range
        if (self.kbegin == 'None' and self.kend == 'None') \
            or (self.kbegin == 'None' and self.kend == lenZ) \
            or (self.kbegin == 0 and self.kend == 'None') \
            or (self.kbegin == 0 and self.kend == lenZ):
            kbeg = 0
            kend = lenZ
            nZ = kend-kbeg
        elif (self.kbegin == 'None' and self.kend != 'None') \
            or (self.kbegin == 0 and self.kend != 'None'):
            kbeg = 0
            kend = int(self.kend)+1
            nZ = kend
        elif (self.kend == 'None' and self.kbegin != 'None') \
            or (self.kend == 0 and self.kbegin != 'None'):
            if self.kbegin > self.kend:
                self.sys.exit("Ending k slice must be greater than begining k slice")
            else:
                kbeg = int(self.kbegin)
                kend = lenZ
                nZ = kend-kbeg
        elif self.kend == self.kbegin:
            kbeg = int(self.kbegin)
            kend = int(self.kend)+1
            nZ = 1
        else:
            kbeg = int(self.kbegin)
            kend = int(self.kend)+1
            nZ = kend-kbeg

        # Set up the time range
        if self.time_begin == 'None' and self.time_end == 'None':
            tbeg = 0
            tend = lenT
            time = tend-tbeg
        elif self.time_begin == 'None':
            tbeg = 0
            tend = self.time_end
            time = tend-tbeg
        elif self.time_end == 'None':
            tbeg = self.time_begin
            tend = lenT
            time = tend-tbeg
        else:
            tbeg = self.time_begin
            tend = lenT
            time = tend-tbeg

        # The number of elements in each dimension will change if it is subsampled
        if self.subsample_num != 'None':
            nX -= nX/self.subsample_num
            nY -= nY/self.subsample_num
            nZ -= nZ/self.subsample_num

        return ibeg, iend, nX, jbeg, jend, nY, kbeg, kend, nZ, tbeg, tend, time

    def subsample( self, data ):
    
        n = self.subsample_num

        if data.ndim == 3:
            z,y,x = data.shape
            z_indices_to_remove = self.np.arange( n-1, z, n )
            y_indices_to_remove = self.np.arange( n-1, y, n )
            x_indices_to_remove = self.np.arange( n-1, x, n )
            z_indices = self.np.delete( self.np.arange(z), z_indices_to_remove )
            y_indices = self.np.delete( self.np.arange(y), y_indices_to_remove )
            x_indices = self.np.delete( self.np.arange(x), x_indices_to_remove )

            # Remove every nth column
            new_data = self.np.take( data, x_indices, 2 )
            # Remove every nth row
            new_data = self.np.take( new_data, y_indices, 1 )
            # Remove every nth layer
            new_data = self.np.take( new_data, z_indices, 0 )
        elif data.ndim == 2:
            y,x = data.shape
            y_indices_to_remove = self.np.arange( n-1, y, n )
            x_indices_to_remove = self.np.arange( n-1, x, n )
            y_indices = self.np.delete( self.np.arange(y), y_indices_to_remove )
            x_indices = self.np.delete( self.np.arange(x), x_indices_to_remove )

            # Remove every nth column
            new_data = self.np.take( data, x_indices, 1 )
            # Remove every nth row
            new_data = self.np.take( new_data, y_indices, 0 )
        elif data.ndim == 1:
            sz = data.shape[0]
            indices_to_remove = self.np.arange( n-1, sz, n )
            indices = self.np.delete( self.np.arange(sz), indices_to_remove )

            # Remove every nth entry
            new_data = self.np.take( data, indices, 0 )

        return new_data
