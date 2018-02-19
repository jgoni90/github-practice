# Create EMME matrices from stacked csv

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:10:56 2018

@author: Jon Goni
"""

# Import relevant libraries
import numpy as np
import pandas as pd
import datetime as dt
import os
import glob

def export_toEMME(df,out_fp,purpose,direction,pop_segment,mode):
    import csv
      
    #Get rid of filtered dimensions
    df = df.groupby(['start_zone_agg','end_zone_agg'], as_index=False)['trips'].sum()
    df['start_zone_agg'] = df.start_zone_agg.apply(lambda x: '{:.0f}'.format(x))
    df['end_zone_agg'] = df.end_zone_agg.apply(lambda x: '{:.0f}'.format(x))
    df['trips'] = df.trips.apply(lambda x: '%.6f' % x)
    
    #Add a blank column in order to create the initial space char in EMME format
    dfexp = pd.DataFrame(columns=['space','O','D','v'])
    
    dfexp.O = df['start_zone_agg'].astype('str')       # The origs column
    dfexp.D = df['end_zone_agg'].astype('str') + ':' # The dests column
    dfexp.v = df['trips'].astype('str')       # The values column
    dfexp.space = ''
    
    emme_mat_name = 'temp1'
    descr = r"Purpose:{} - Direction:{} - Population Segment:{} - Mode:{}".format(purpose,direction,pop_segment,mode)
    
    hline_1 = r't matrices'
    hline_2 = r'd matrix= mf001'
    hline_3 = r"a matrix= mf001 {} 0 '{}'".format(emme_mat_name,descr)
    lines = '\n'.join([hline_1,hline_2,hline_3])
    
    text_file = open(out_fp, 'w')
    text_file.write(lines)
    text_file.write('\n')
    text_file.close()
    
    dfexp.to_csv(out_fp,index=False,header=False,mode='a',sep=' ', quoting=csv.QUOTE_NONE, float_format='%.3f')

# Delete previous outputs, if they exist
for f in glob.glob(r'..\Output\MND_*.txt'):
    os.remove(f)

# Read Dataframe
df = pd.read_csv(r'..\Output\Data.csv',low_memory=False)

# Unpivot mode columns
df = pd.melt(df, id_vars=['start_zone_agg',
                          'end_zone_agg',
                          'purpose',
                          'direction',
                          'resident'],
             value_vars=['trips_pt',
                         'trips_car',
                         'trips_cab',
                         'trips_phv',
                         'trips_lgv',
                         'trips_hgv',
                         'trips_cycle',
                         'trips_walk'],
             var_name='mode', value_name='trips')

df['mode'] = df['mode'].str.replace('trips_','')

# Create category arrays
purposes = ['HBW', 'HBE', 'HBO', 'NHB']
directions = ['OB', 'IB']
pop_segments = ['GLA', 'REST_UK', 'IR']
modes = ['pt', 'car', 'cab', 'phv', 'lgv', 'hgv', 'cycle', 'walk']

# Loop through each category to create separate matrices
for purpose in purposes:
    for pop_segment in pop_segments:
        for mode in modes:
            if purpose == 'NHB':
                df_i = df[(df['purpose']==purpose) & (df['resident']==pop_segment) & (df['mode']==mode) & pd.notnull(df['trips'])]
                df_i = df_i[df_i['trips']!='(null)']
                df_i['trips'] = df_i.trips.astype(float)
                if df_i.empty:
                    print('Dataframe for {}, {}, {} is empty!'.format(purpose,pop_segment,mode))
                else:
                    export_toEMME(df_i,r'..\Output\MND_{}_None_{}_{}.txt'.format(purpose,pop_segment,mode),purpose,'None',pop_segment,mode)
            else:
                for direction in directions:
                    df_i = df[(df['purpose']==purpose) & (df['direction']==direction) & (df['resident']==pop_segment) & (df['mode']==mode) & pd.notnull(df['trips'])]
                    if df_i.empty:
                        print('Dataframe for {}, {}, {}, {} is empty!'.format(purpose,direction,pop_segment,mode))
                    else:
                        export_toEMME(df_i,r'..\Output\MND_{}_{}_{}_{}.txt'.format(purpose,direction,pop_segment,mode),purpose,direction,pop_segment,mode)