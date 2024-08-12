import pandas as pd

# Read the CSV file
df = pd.read_csv('DEPARTAMENTOS.csv')

# Create a new DataFrame to store the unique values
unique_values_df = pd.DataFrame(columns=['Column', 'Unique Values'])

# Iterate over each column
for column in df.columns:
    # Get the unique values in the column
    unique_values = df[column].unique()
    
    df[column].value_counts().to_csv('count_'+column+'.csv')
