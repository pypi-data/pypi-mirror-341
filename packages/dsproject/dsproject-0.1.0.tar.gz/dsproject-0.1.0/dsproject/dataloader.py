import pandas as pd

def load_data(filepath='data/data.csv'):
    df = pd.read_csv(filepath)
    return df
