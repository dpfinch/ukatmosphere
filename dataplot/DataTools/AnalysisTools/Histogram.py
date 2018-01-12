#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# modulename
#import modulename
#==============================================================================

def Histogram(arg):
    """
        Description of function here
        Function IN:
            argin (REQUIRED, DTYPE):
                Description of the argument in, wheter its REQUIRED, OPTIONAL,
                and what is DEFAULT
        Fucntion OUT:
            argout:
                Description of what the fuction returns if any
    """
    print('Histogram Test')
    pass

if __name__ == '__main__':
    # If the module needs testing as a stand alone, use this to set the
    # paramters
    filename  = 'RawData/Heathfield' \
                    + 'GAUGE-CRDS_HFD_20130101_ch4-100m.nc'
    Histogram(filename)
## ============================================================================
## END OF PROGAM
## ============================================================================
