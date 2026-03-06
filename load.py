import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text 

def align_sequences(engine):
    print("Aligning ID counters in postgres")
    
    dictids = {
        "status": "statusid",
        "constructors": "constructorid",
        "circuits": "circuitid",
        "drivers": "driverid",
        "races": "raceid",
        "results": "resultid"
    }
    
    with engine.connect() as connection:
        for table, pk in dictids.items():
            query = text(f"SELECT setval(pg_get_serial_sequence('{table}', '{pk}'), COALESCE(MAX({pk}), 1)) FROM {table};")
            
            connection.execute(query)
            connection.commit()  
            print(f"Sequence aligned for table: {table}")

df_raw = pd.read_csv('f1.csv', low_memory=False) 

df_ready = df_raw.copy()

df_ready.replace(r'^\\N$', np.nan, regex=True, inplace=True)

df_drivers = df_ready[['driverId', 'forename', 'surname', 'number_y', 'code', 'dob', 'nationality_driver', 'url_driver']].drop_duplicates(subset=['driverId'])
df_drivers.columns = ['driverid', 'name', 'surname', 'number', 'code', 'dob', 'nationality', 'url']

df_drivers['code'] = df_drivers['code'].str.upper()
df_drivers['number'] = pd.to_numeric(df_drivers['number'])
df_drivers['number'] = df_drivers['number'].replace(0, np.nan)
df_drivers.loc[df_drivers['code'].str.len() != 3, 'code'] = np.nan

df_constructors = df_ready[['constructorId', 'name', 'nationality_constructor', 'url_constructor']].drop_duplicates(subset=['constructorId'])
df_constructors.columns = ['constructorid', 'name', 'nationality', 'url']

df_circuits = df_ready[['circuitId', 'name_y', 'location', 'country', 'lat', 'lng', 'alt', 'url_y']].drop_duplicates(subset=['circuitId'])
df_circuits.columns = ['circuitid', 'name', 'location', 'country', 'lat', 'lng', 'alt', 'url']

df_status = df_ready[['statusId', 'status']].drop_duplicates(subset=['statusId'])
df_status.columns = ['statusid', 'status']
colonne_races = ['raceId', 'year', 'round', 'circuitId', 'name_x', 'date', 'time_race', 'url_x', 
                 'quali_date', 'quali_time', 'sprint_date', 'sprint_time']
df_races = df_ready[colonne_races].drop_duplicates(subset=['raceId'])
df_races.columns = ['raceid', 'year', 'round', 'circuitid', 'name', 'date', 'time_race', 'url', 
                    'quali_date', 'quali_time', 'sprint_date', 'sprint_time']

colonne_results = ['resultId', 'raceId', 'driverId', 'constructorId', 'statusId', 'number_x', 'grid', 
                   'position', 'positionText', 'positionOrder', 'points', 'laps', 
                   'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed']
df_results = df_ready[colonne_results].drop_duplicates(subset=['resultId'])
df_results.columns = ['resultid', 'raceid', 'driverid', 'constructorid', 'statusid', 'number', 'grid', 
                      'position', 'positiontext', 'positionorder', 'points', 'laps', 
                      'milliseconds', 'fastestlap', 'rank', 'fastestlaptime', 'fastestlapspeed']

lista_df = [df_drivers, df_constructors, df_circuits, df_status, df_races, df_results]
for i in range(len(lista_df)):
    lista_df[i] = lista_df[i].astype(object).where(pd.notna(lista_df[i]), None)

df_drivers, df_constructors, df_circuits, df_status, df_races, df_results = lista_df

db_url = "postgresql://postgres:password@db:5432/f1db"
engine = create_engine(db_url)

df_drivers.to_sql('drivers', engine, if_exists='append', index=False, chunksize=500)
df_constructors.to_sql('constructors', engine, if_exists='append', index=False, chunksize=500)
df_circuits.to_sql('circuits', engine, if_exists='append', index=False, chunksize=500)
df_status.to_sql('status', engine, if_exists='append', index=False, chunksize=500)
df_races.to_sql('races', engine, if_exists='append', index=False, chunksize=500)
df_results.to_sql('results', engine, if_exists='append', index=False, chunksize=500)

align_sequences(engine)

print("Dati caricati in PostgreSQL con successo!")