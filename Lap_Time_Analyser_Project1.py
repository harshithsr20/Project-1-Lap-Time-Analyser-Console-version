import pandas as pd
import numpy as np
try:
    og_laptimes=pd.read_csv('lap_time.csv')
    if 'LapNumber' not in og_laptimes.columns:
        print('No Lap Numbers given')
        exit()
    if 'LapTime'  not in og_laptimes.columns:
        print('No Lap Times given')
        exit()

except FileNotFoundError:
    print('File not found')
    exit()

# Data Cleaning
#Name cleaning
og_laptimes['Driver']=og_laptimes.groupby('Car')['Driver'].bfill().ffill()
#Car Cleaning
og_laptimes['Car']=og_laptimes.groupby('Driver')['Car'].ffill().bfill()
#LapNumber cleaning
og_laptimes['LapNumber']=pd.to_numeric(og_laptimes['LapNumber'],errors='coerce')
og_laptimes['LapNumber']=og_laptimes['LapNumber'].fillna(og_laptimes['LapNumber'].interpolate())
og_laptimes=og_laptimes[og_laptimes['LapNumber']>0]
og_laptimes['LapNumber'].drop_duplicates(inplace=True)
#Laptime cleaning
og_laptimes['LapTime']=pd.to_numeric(og_laptimes['LapTime'],errors='coerce')
og_laptimes['LapTime']=og_laptimes.groupby(['Driver','Stint'])['LapTime'].bfill().ffill()
#Stint number cleaning
og_laptimes['Stint']=pd.to_numeric(og_laptimes['Stint'],errors='coerce')
og_laptimes.loc[og_laptimes['Stint']<0,og_laptimes['Stint']]=pd.NA
og_laptimes['Stint']=og_laptimes.groupby('Driver')['Stint'].ffill().bfill()


