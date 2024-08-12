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

#remover los vaciós o la basura prococada por alerts y conteo entre los datos
regex = r"([0-9]+( )*Establecimientos encontrados|alert\('.*'\))"
unvalid = (df['CODIGO'].str.contains(regex).astype(bool))
df = df.loc[~unvalid]


#Limpiar los valores de  Código
'''
Eliminación de valores no numéricos, para que sea un valor numérico
ejemplo : 4451-4451 a 44514451
'''
df['CODIGO'] = df['CODIGO'].str.replace('-', '')
print(df['CODIGO'].head())


#limpiar los números telefónicos
'''
Eliminación de valores no numéricos, es decir los guiones
En caso de no haber entrada, reemplazar por string de 8 0’s
'''
df['TELEFONO'] = df['TELEFONO'].str.replace('-', '')
df['TELEFONO'] = df['TELEFONO'].fillna('00000000')
print(df['TELEFONO'].head())
#limpiar los valores de nombres de establecimientos
'''
Convertir a mayúsculas para uniformidad
aplicar utf8 de encoding para evitar problemas con tildes. 

'''
raise NotImplementedError("limpiar los valores de nombres de establecimientos")

#limpiar las direcciones
'''
Dirección
Normalizar abreviaturas, es decir Avenida a Av. 
Convertir a mayúsculas para uniformidad
''' 
raise NotImplementedError("limpiar las direcciones")


#guardar en un CSV
df.dropna(how="all")
df.to_csv('DEPARTAMENTOS.csv',index=False)
del raw_dfs
del df