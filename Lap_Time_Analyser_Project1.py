import pandas as pd
import numpy as np
try:
    og_laptimes=pd.read_csv(input('Enter the File path'))
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
    blap=driver_df['LapTime'].min()
    wlap=driver_df['LapTime'].max()
    meanlap=driver_df['LapTime'].mean().round(3)
    medlap=driver_df['LapTime'].median().round(3)
    stddev=driver_df['LapTime'].std().round(3)
    #deg analysis
    deltlaps=driver_df['LapTime'].diff()
    driver_df['Delta_wrt_last_lap']=deltlaps
    driver_df['Delta_wrt_best_lap']=driver_df['LapTime'].apply(lambda x:round(x-blap,3))
    deg=deltlaps.mean().round(3)
    driver_df['rolling']=driver_df['LapTime'].rolling(3).mean()
    gainmaxlap=np.argmin(deltlaps)
    degmaxlap=np.argmax(deltlaps)

    #Outlier conditions were set and given by chatgpt as I do not know based on what metrics should I divide outliers from the normal dataset
    driver_df['Outlier_flag']=driver_df['LapTime'].apply(lambda x:"Possible Traffic/SC/VSC/Chaotic Race" if abs(x-meanlap)>2*stddev else np.nan)
    stddev=driver_df.drop(driver_df[abs(driver_df['LapTime']-meanlap)>2*stddev].index)['LapTime'].std().round(3)
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
    if driver_df['Outlier_flag'].count()/driver_df['LapTime'].count()<0.25:
        verdict3="Clean Race"
    else:
         verdict3="Too much Traffic or VSC/Chaotic Race"
    driver_df=driver_df[['Driver','Car','LapNumber','Stint','LapTime','Delta_wrt_last_lap','Delta_wrt_best_lap','TyreCompound','Timestamp','Outlier_flag']]
    return driver_df,blap,wlap,meanlap,medlap,stddev,deltlaps,deg,gainmaxlap,degmaxlap,verdict1,verdict2,verdict3
def display(n):
    dtable, flap, slap, mlap, melap, std, delt, deg,gainmax, degmax, v1, v2, v3=analyse(n)
    drivernames={'VER':'Max Verstappen','HAM':'Lewis Hamilton','NOR':'Lando Norris','LEC':'Charles Leclerc'}
    with open('output.txt',"w") as f:
        f.write('\t\t\t\t\t--------Driver Data--------\n')
        f.write(f'Driver Name:{drivernames[n]}\n')
        f.write('Driver Data:\n')
        f.write(dtable.to_string())
        f.write('\n\n-----STATS------')
        f.write(f'\n\nFastest Lap:{flap} secs\n')
        f.write(f'Slowest Lap:{slap} secs\n')
        f.write(f'Median Lap:{melap} secs\n')
        f.write(f'Average Lap:{mlap} secs\n')
        f.write(f'Standard Deviation/Consistency:{std} secs\n')
        f.write(f'Degradation rate:{deg}sec/lap\n')
        f.write(f'Best delta was gained on lap:{gainmax}\n')
        f.write(f'Delta was degraded on lap:{degmax}\n')
        outcount=dtable['Outlier_flag'].count()
        f.write(f'Outliers Detected:{outcount}\n')
        f.write('\n\n')
        f.write(f'VERDICT:\n')
        f.write(f'1. {v1}\n')
        f.write(f'2. {v2}\n')
        f.write(f'3. {v3}\n')

def main():
    print('--------Lap Time Analyser------------')
    print('Available Drivers:')
    driverlist=og_laptimes['Driver'].unique()
    for i,j in enumerate(driverlist):
        print(f'{i+1}. {j}')
    display(input('Enter the Driver Name(CODE FORM!):'))
main()