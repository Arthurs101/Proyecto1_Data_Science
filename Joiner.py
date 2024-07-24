import os
import pandas as pd
#combine all the csv files into a single one
df = pd.DataFrame()
raw_dfs = []
for raw_department in os.listdir('./RAW_FILES'):
    # crea columnas "UNNAMED" al leer el csv, el.loc las elemina
    raw_df = pd.read_csv("./RAW_FILES/"+ raw_department,skiprows=1)
    raw_df = raw_df.loc[:, ~raw_df.columns.str.contains('^Unnamed')]
    raw_dfs.append(raw_df)
df = pd.concat(raw_dfs,ignore_index=True)
df.to_csv('DEPARTAMENTOS.csv',index=False)
del raw_dfs
del df