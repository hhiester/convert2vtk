import sys
import os

# Path to libs
sys.path.append("/panfs/storage.local/coaps/home/ndc08/code/converter/libs/lib64")
# Path to modules
sys.path.append("/panfs/storage.local/coaps/home/ndc08/code/converter/modules")

class convert2vtk():
    """ Read in a model's output data file

            Currently supports:
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


    def __init__( self, init_vars ):
        """ Initialization Routine - Create the output folder to hold the vtk files 
        init_vars - dictionary of initialization variables"""
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
        self.time_step = init_vars['time_step']
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
        print "In the __del__ routine"

        return


    def __load( self ):
        """ Load the initialization variables into memory for conversion. """ 
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

            print "The file read in \n\n", self.input_filename.split("/")[-1], \
                    "is a", self.filetype, "file."

# ---------------------------------- Unrecognized files -------------------------------

        else:
            sys.exit( "\nERROR: The filetype to be converted \n\n%s\n\n" % self.input_filename+ \
                    "is not recognized!\n")
 
       

    def convert( self ):
        """ Convert the input file(s) into vtk file(s) """
        print "In the convert routine"

        if self.filetype == "hycom_binary":
            self.__convertHycomB()
        elif self.filetype == "hycom_z":
            self.__convertHycomZ()
        elif self.filetype == "ncom":
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
