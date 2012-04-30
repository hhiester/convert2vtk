import glob, os, sys, unittest, netCDF4
sys.path.append("build/temp.linux-x86_64-2.6")
from netCDF4 import getlibversion,__hdf5libversion__,__netcdf4libversion__,__version__

__all__ = ['test']
# Find all test files.
test_files = glob.glob('tst_*.py')
py_path = os.environ.get('PYTHONPATH')
if py_path is None:
    py_path = '.'
else:
    py_path = os.pathsep.join(['.',py_path])
os.environ['PYTHONPATH'] = py_path

# Build the test suite from the tests found in the test files.
testsuite = unittest.TestSuite()
version = getlibversion().split()[0]
for f in test_files:
    m = __import__(os.path.splitext(f)[0])
    testsuite.addTests(unittest.TestLoader().loadTestsFromModule(m))

# Run the test suite. 


def test(verbosity=1):
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(testsuite)

if __name__ == '__main__':
    test(verbosity=1)
    import sys
    sys.stdout.write('\n')
    sys.stdout.write('netcdf4-python version: %s\n' % __version__)
    sys.stdout.write('HDF5 lib version:       %s\n' % __hdf5libversion__)
    sys.stdout.write('netcdf lib version:     %s\n' % __netcdf4libversion__)
