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
og_laptimes['Driver']=og_laptimes.groupby('Car')['Driver'].ffill()

#Car Cleaning
og_laptimes['Car']=og_laptimes.groupby('Driver')['Car'].ffill().bfill().str.upper()
#LapNumber cleaning
og_laptimes['LapNumber']=pd.to_numeric(og_laptimes['LapNumber'],errors='coerce')
og_laptimes['LapNumber']=og_laptimes['LapNumber'].fillna(og_laptimes['LapNumber'].interpolate())
og_laptimes=og_laptimes[og_laptimes['LapNumber']>0]
og_laptimes['LapNumber'].drop_duplicates(inplace=True)
#Laptime cleaning
og_laptimes['LapTime']=pd.to_numeric(og_laptimes['LapTime'],errors='coerce')
og_laptimes['LapTime'].dropna(inplace=True)
#Stint number cleaning
og_laptimes['Stint']=pd.to_numeric(og_laptimes['Stint'],errors='coerce')
og_laptimes.loc[og_laptimes['Stint']<0,'Stint']=pd.NA
og_laptimes['Stint']=og_laptimes.groupby('Driver')['Stint'].ffill().bfill()
#Tyre Compound Cleaning
og_laptimes['TyreCompound']=og_laptimes['TyreCompound'].replace({'S':'Soft','M':'Medium','H':'Hard'}).str.upper()
#TimeStamp cleaning
og_laptimes['Timestamp']=pd.to_datetime(og_laptimes['Timestamp'],errors='coerce')

def analyse(name):
    dn=name
    driver_df=og_laptimes[og_laptimes['Driver']==dn].reset_index(drop=True)
    print(driver_df)
    blap=driver_df['LapTime'].min().round(3)
    wlap=driver_df['LapTime'].max().round(3)
    meanlap=driver_df['LapTime'].mean().round(3)
    medlap=driver_df['LapTime'].median().round(3)
    stddev=driver_df['LapTime'].std().round(3)
    #deg analysis
    deltlaps=driver_df['LapTime'].diff()
    deg=deltlaps.mean().round(3)
    driver_df['rolling']=driver_df['LapTime'].rolling(3).mean()
    implaps=0
    deglaps=0
    for i in deltlaps:
        if i<0:
            implaps+=1
        else:
            deglaps+=1
    gainmaxlap=np.argmin(deltlaps)
    degmaxlap=np.argmax(deltlaps)
    driver_df['OutLier Flag']=np.where(driver_df['LapTime']>driver_df.LapTime.quantile(0.75),"Possible Traffic or VSC",np.nan)
    verdict1=""
    verdict2=""
    verdict3=""
    if stddev<0.4:
        verdict1="High Consistency"
    else:
        verdict1="Low/Inconsistent"
    if deg>0.08:
        verdict2="High Tyre Degradation"
    else:
        verdict2="Low Tyre Degradation"
    if driver_df.count()<1:
        verdict3="Clean Race"
    else:
         verdict3="Too much Traffic or VSC/Chaotic Race"
    return driver_df,blap,wlap,meanlap,medlap,stddev,deltlaps,deg,implaps,deglaps,gainmaxlap,degmaxlap,verdict1,verdict2,verdict3
def display(n):
    dtable, flap, slap, mlap, melap, std, delt, deg, implc, deglc,gainmax, degmax, v1, v2, v3=analyse(n)


def main():
    print('--------Lap Time Analyser------------')
    print('Available Drivers:')
    driverlist=og_laptimes['Driver'].unique()
    for i,j in enumerate(driverlist):
        print(f'{i+1}. {j}')
    analyse('VER')
main()