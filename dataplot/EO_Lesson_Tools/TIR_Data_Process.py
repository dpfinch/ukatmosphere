### ===================================================================
### Deal with the data from the TIR camera of the example data
### ===================================================================
#
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import math
import string


def from_3d_numpy_to_pd(inarray):
    if len(inarray.shape) == 3:
        steps = inarray.shape[0]
    elif len(inarray.shape) == 2:
        steps = 1

    # This assumes a pixel shape of 32x32 - might need to change this
    reshaped = inarray.reshape([32*steps,32])

    labels = ['Pixel {}'.format(x) for x in range(32)]
    new_df = pd.DataFrame(reshaped, index = range(reshaped.shape[0]),
        columns = labels)

    return new_df

def from_pd_to_3d_numpy(df):
    values = df.values
    # Assumes pixel array of 32x32
    new_arr = values.reshape([int(values.shape[0]/32),32,32])
    return new_arr

def from_stored_json(stored_data):
    df = pd.read_json(stored_data,orient = 'split')
    new_arr = from_pd_to_3d_numpy(df)
    return new_arr

def prettify_data_for_table(df, frame_num = 1):
    df = pd.read_json(stored_data,orient = 'split')
    new_arr = from_pd_to_3d_numpy(df)

    frame = new_arr[frame_num - 1]

    labels = ['Pixel {}'.format(x) for x in range(32)]
    new_df = pd.DataFrame(frame, index = range(32)+1, columns = labels)

    return new_df
