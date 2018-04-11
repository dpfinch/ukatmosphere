import os
from datetime import datetime as dt
import pandas
from dataplot.models import measurement_data, measurement_info, site_info


### Need to have a table to have all the information about the sites
### Won't be updated often but will be every now and again
### Will need some sort of method to update it automatically when needed

### The same will apply to the measurement info database. Need to be careful
### about subtly different measurement ids, eg different unit

### The measurement data table will do most of the hard work. It will need
### to be constantly updated from lots of different sources
