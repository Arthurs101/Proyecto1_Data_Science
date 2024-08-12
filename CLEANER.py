import os
import pandas as pd
import numpy as np

# Combinar todos los archivos CSV en un único DataFrame
df = pd.DataFrame()
raw_dfs = []

for raw_department in os.listdir('./RAW_FILES'):
    '''
    Leer el CSV y eliminar columnas "UNNAMED" que son innecesarias
    '''
    raw_df = pd.read_csv("./RAW_FILES/" + raw_department, skiprows=1)
    raw_df = raw_df.loc[:, ~raw_df.columns.str.contains('^Unnamed')]
    raw_dfs.append(raw_df)

# Concatenar todos los DataFrames en uno solo
df = pd.concat(raw_dfs, ignore_index=True)

# Remover filas que contienen valores no válidos o basura
regex = r"([0-9]+( )*Establecimientos encontrados|alert\('.*'\))"
unvalid = df['CODIGO'].str.contains(regex).astype(bool)
df = df.loc[~unvalid]

# Limpiar los valores de Código
df['CODIGO'] = df['CODIGO'].str.replace('-', '')
print("Limpieza de CODIGO completada:")
print(df['CODIGO'].head())

# Limpiar los números telefónicos
df['TELEFONO'] = df['TELEFONO'].str.replace('-', '').str.strip()
df['Numero Adicional'] = np.where(df['TELEFONO'].str.len() < 8, df['TELEFONO'], np.nan)
df['TELEFONO'] = np.where(df['TELEFONO'].str.len() >= 8, df['TELEFONO'], np.nan)
print("Limpieza de TELEFONO completada:")
print(df[['TELEFONO', 'Numero Adicional']].head())

# Limpiar los valores de nombres de establecimientos y mantener el original
df['ESTABLECIMIENTO ORIGINAL'] = df['ESTABLECIMIENTO']
df['ESTABLECIMIENTO'] = df['ESTABLECIMIENTO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.upper()
print("Limpieza de ESTABLECIMIENTO completada:")
print(df[['ESTABLECIMIENTO', 'ESTABLECIMIENTO ORIGINAL']].head())

# Limpiar las direcciones
df['DIRECCION'] = df['DIRECCION'].str.upper()
df['DIRECCION'] = df['DIRECCION'].str.replace('AVENIDA', 'AV.')
df['DIRECCION'] = df['DIRECCION'].str.replace('CALLE', 'C.')
df['DIRECCION'] = df['DIRECCION'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
print("Limpieza de DIRECCION completada:")
print(df['DIRECCION'].head())

# Limpiar los valores de Supervisor y Director
df['SUPERVISOR'] = df['SUPERVISOR'].str.upper().fillna(np.nan)
df['DIRECTOR'] = df['DIRECTOR'].str.upper().fillna(np.nan)
print("Limpieza de SUPERVISOR y DIRECTOR completada:")
print(df[['SUPERVISOR', 'DIRECTOR']].head())

# Remover filas duplicadas basadas en la columna ESTABLECIMIENTO
df = df.drop_duplicates(subset=['ESTABLECIMIENTO'], keep=False)
print("Duplicados eliminados:")
print(df.shape)

# Remover filas completamente vacías (por si quedaron después de la limpieza)
df.dropna(how="all", inplace=True)

# Guardar el DataFrame limpio en un archivo CSV
df.to_csv('DEPARTAMENTOS.csv', index=False)

# Limpieza finalizada, liberar memoria
del raw_dfs
del df

print("Proceso de limpieza completado y datos guardados en 'DEPARTAMENTOS.csv'")
