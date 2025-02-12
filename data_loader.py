import pandas as pd
import numpy as np 


def load_data(path:str):
    """Oil losses data from a CSV file.
    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """
    data = pd.read_csv(path)
    data = data[data['Subsidiary'].isin(['BIR', 'CAD', 'CG', 'CMI', 'COQ', 'GAE', 'GUT', 'MIX', 'TOD', 'TIN', 'TOR', 'TOTO', 'KFC', 'WSK' ,'VIN'])]
    return data

def preprocess_data(data): 
    data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y %H:%M')

    full_range = pd.date_range(start=data['date'].min(), end=data['date'].max())
    data = data.iloc[:, :4] 
    data.columns = ["date", "Subsidiary", "Oil losses (bopd)", "Wells WWO"]

    grouped_data = data.groupby(['date', 'Subsidiary'])['Oil losses (bopd)'].sum().unstack()  # Desapilar por Subsidiary
    grouped_data = grouped_data.reindex(full_range, fill_value=0)
    losses = grouped_data.fillna(0)

    subsidiaries = grouped_data.columns
    dates = grouped_data.index

    wells = data.groupby(data['date'].dt.to_period('D'))['Wells WWO'].sum()
    wells_cumsum = wells.cumsum()

    print(f"Data load OK :start:")

    return (full_range, dates, subsidiaries, wells, losses)

df = load_data("data/Libro1.csv")
full_range, dates, subsidiaries, wells, losses = preprocess_data(df)


