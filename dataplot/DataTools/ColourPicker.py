#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# brewer2mpl
import brewer2mpl
#==============================================================================

def GetQualitative(themename = 'Set1'):
    """
        Return an array of colours as an RGB string to use - the size of array
        depends on requested by the user.
        Function IN:
            themename (OPTIONAL, STRING ):
                The colour theme (default = 'Set1')
        Fucntion OUT:
            colour_array:
                An an array containing the number of colours requested as
                RGB string.
    """


    bmap = brewer2mpl.get_map(themename, 'Qualitative', 8)

    colour_array = []
    # Loop through all the colours and make them a string
    for col in bmap.colors:
        R = col[0]
        G = col[1]
        B = col[2]
        colour_array.append('rgb(%d,%d,%d)' % (R,G,B) )

    return colour_array

## ============================================================================
## END OF PROGRAM
## ============================================================================
