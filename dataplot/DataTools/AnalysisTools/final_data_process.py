#==============================================================================
# Description of module here
#
#==============================================================================
# Uses modules:
# modulename
#==============================================================================

def returnXY(df_column, **kwargs):
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
    kwargs = kwargs['kwargs']
    resample_rate = kwargs['DataResample'][0]
    if resample_rate == 'R':
        resampled_df = df_column
    else:
        resampled_df = df_column.resample(resample_rate).apply('mean')

    # Apply time range
    date_range = kwargs['date_range']
    resampled_df = resampled_df[date_range[0]:date_range[1]]

    x = resampled_df.index
    y = resampled_df

    return x, y

## ============================================================================
## END OF PROGAM
## ============================================================================
