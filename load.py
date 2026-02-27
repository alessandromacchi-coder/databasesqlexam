import pandas as pd
import sqlite3
import numpy as np

df_raw = pd.read_csv('f1.csv', low_memory=False) #il low memory per 

df_ready = df_raw.copy()

df_ready.replace(r'^\\N$', np.nan, regex=True, inplace=True)

df_drivers = df_ready[['driverId', 'forename', 'surname', 'number_y', 'code', 'dob', 'nationality_driver', 'url_driver']].drop_duplicates(subset=['driverId'])

df_drivers.columns = ['driverid', 'name', 'surname', 'number', 'code', 'dob', 'nationality', 'url']

df_drivers['code'] = df_drivers['code'].str.upper()
df_drivers['number'] = pd.to_numeric(df_drivers['number'])

df_constructors = df_ready[['constructorId', 'name', 'nationality_constructor', 'url_constructor']].drop_duplicates(subset=['constructorId'])
df_constructors.columns = ['constructorid', 'name', 'nationality', 'url']

df_circuits = df_ready[['circuitId', 'name_y', 'location', 'country', 'lat', 'lng', 'alt', 'url_y']].drop_duplicates(subset=['circuitId'])
df_circuits.columns = ['circuitid', 'name', 'location', 'country', 'lat', 'lng', 'alt', 'url']

df_status = df_ready[['statusId', 'status']].drop_duplicates(subset=['statusId'])
df_status.columns = ['statusid', 'status']

colonne_races = ['raceId', 'year', 'round', 'circuitId', 'name_x', 'date', 'time_race', 'url_x', 
                 'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 
                 'quali_date', 'quali_time', 'sprint_date', 'sprint_time']
df_races = df_ready[colonne_races].drop_duplicates(subset=['raceId'])
df_races.columns = ['raceid', 'year', 'round', 'circuitid', 'name', 'date', 'time_race', 'url', 
                    'fp1_date', 'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date', 'fp3_time', 
                    'quali_date', 'quali_time', 'sprint_date', 'sprint_time']

colonne_results = ['resultId', 'raceId', 'driverId', 'constructorId', 'statusId', 'number_x', 'grid', 
                   'position', 'positionText', 'positionOrder', 'points', 'laps', 'time_result', 
                   'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed']
df_results = df_ready[colonne_results].drop_duplicates(subset=['resultId'])
df_results.columns = ['resultid', 'raceid', 'driverid', 'constructorid', 'statusid', 'number', 'grid', 
                      'position', 'positionText', 'positionOrder', 'points', 'laps', 'time_result', 
                      'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed']


dbpath = "f1.db"
conn = sqlite3.connect(dbpath)

df_drivers.to_sql('drivers', conn, if_exists='append', index=False)
df_constructors.to_sql('constructors', conn, if_exists='append', index=False)
df_circuits.to_sql('circuits', conn, if_exists='append', index=False)
df_status.to_sql('status', conn, if_exists='append', index=False)
df_races.to_sql('races', conn, if_exists='append', index=False)
df_results.to_sql('results', conn, if_exists='append', index=False)

print("file .db caricato con successo")
conn.close()