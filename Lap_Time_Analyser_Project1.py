import numpy as np
import pandas as pd

og_lap_times=pd.read_csv("/Python pactice for motorsport/monaco_2025_dirty_laps.csv")
print(og_lap_times)

# Data Cleaning
og_lap_times.columns=og_lap_times.columns.str.strip().str.replace(" ","_")
og_lap_times['lap_number']=pd.to_numeric(og_lap_times['lap_number'],errors='coerce')
og_lap_times['lap_time_seconds']=pd.to_numeric(og_lap_times['lap_time_seconds'],errors='coerce')
og_lap_times['lap_number']=og_lap_times['lap_number'].fillna(og_lap_times.index.to_series()+1)
'''Code line 11 from chatgpt I could not figure out a way to replace NaN values with the index+! of the values'''
avg_lap_times=og_lap_times['lap_time_seconds'].mean()
og_lap_times['lap_time_seconds']=og_lap_times['lap_time_seconds'].fillna(og_lap_times['lap_time_seconds'].interpolate())
'''Learnt about interpolate function'''
print(og_lap_times.head(20))
