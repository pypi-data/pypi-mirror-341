import pandas as pd

# Load data from csv
# data = pd.read_csv('data.csv')

def load_csv_pandas(filename, separator=',', delimiter='"'):
    # Load the CSV file using pandas:
    data = pd.read_csv(filename)
    return data.iterrows()