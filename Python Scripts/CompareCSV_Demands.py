# -*- coding: utf-8 -*-
# Process to compare two input demand csv files, using pandas#
# Version 1.0 - Jon Goni#
"""
Created on Thu Jan 19 11:03:15 2017

@author: goniuj
"""

# Import relevant libraries:
import pandas as pd
import os

# Specify comparison years
year1 = '2015'
year2 = '2021'

# Specify origin and destination directories
basepath1 = 'U:\HEIDI_SERTM\Forecasting\{}bs_v001\Demand'.format(year1)
basepath2 = 'U:\HEIDI_SERTM\Forecasting\{}bs_v001\Demand'.format(year2)
newfolder = 'Demand_Comparison'
newpath = os.path.join(basepath1.rsplit("\\", 1)[0], newfolder)

# Check existence of destination folder, create if needed
if not os.path.exists(newpath):
    os.makedirs(newpath)

dtype = 'Goods'
fname = 'Input_Demand{}.csv'.format(dtype)
path1 = os.path.join(basepath1, fname)
path2 = os.path.join(basepath2, fname)
newfile = '{}vs{}_{}.csv'.format(year1, year2, dtype)

if 'PTtrips' in fname:
    sr = 4
else:
    sr = 0

# Read .csv files as dataframes
df1 = pd.read_csv(path1, header=None, skiprows=sr)
df1.columns = ['LoopID', 'OriginID', 'DestinationID',
               'SegmentID', 'ModeID', 'TimeID', 'Demand1']
df2 = pd.read_csv(path2, header=None, skiprows=sr)
df2.columns = ['LoopID', 'OriginID', 'DestinationID',
               'SegmentID', 'ModeID', 'TimeID', 'Demand2']

# Merge matching values into new dataframe
mergedf = pd.merge(df1, df2,
                   left_on=['LoopID', 'OriginID', 'DestinationID',
                            'SegmentID', 'ModeID', 'TimeID'],
                   right_on=['LoopID', 'OriginID', 'DestinationID',
                             'SegmentID', 'ModeID', 'TimeID'])

# Compute demand differences
mergedf['D_Diff'] = mergedf['Demand2'] - mergedf['Demand1']

# Delete previous columns
mergedf = mergedf.drop(['Demand1', 'Demand2'], axis=1)

# Write output dataframe to new csv file
mergedf.to_csv(os.path.join(newpath, newfile),
               header=None, index=False, float_format='%.3f')
