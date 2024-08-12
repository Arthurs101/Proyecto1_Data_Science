import os
import pandas as pd

# Combinar todos los archivos CSV en un único DataFrame
df = pd.DataFrame()
raw_dfs = []

for raw_department in os.listdir('./RAW_FILES'):
    '''
    Leer el CSV y eliminar columnas "UNNAMED" que son innecesarias
    '''
    raw_df = pd.read_csv("./RAW_FILES/"+ raw_department, skiprows=1)
    raw_df = raw_df.loc[:, ~raw_df.columns.str.contains('^Unnamed')]
    raw_dfs.append(raw_df)

# Concatenar todos los DataFrames en uno solo
df = pd.concat(raw_dfs, ignore_index=True)

# Remover filas que contienen valores no válidos o basura
'''
Remover filas que contienen valores como "Establecimientos encontrados" o alertas
'''
regex = r"([0-9]+( )*Establecimientos encontrados|alert\('.*'\))"
unvalid = df['CODIGO'].str.contains(regex).astype(bool)
df = df.loc[~unvalid]

# Limpiar los valores de Código
'''
Eliminación de valores no numéricos para que sea un valor numérico.
Por ejemplo, convertir "4451-4451" a "44514451"
'''
df['CODIGO'] = df['CODIGO'].str.replace('-', '')
print("Limpieza de CODIGO completada:")
print(df['CODIGO'].head())

# Limpiar los números telefónicos
'''
Eliminación de valores no numéricos, es decir los guiones.
En caso de no haber entrada, reemplazar por string de 8 0’s "00000000".
'''
df['TELEFONO'] = df['TELEFONO'].str.replace('-', '')
df['TELEFONO'] = df['TELEFONO'].fillna('00000000')
print("Limpieza de TELEFONO completada:")
print(df['TELEFONO'].head())

# Limpiar los valores de nombres de establecimientos
'''
Convertir a mayúsculas para uniformidad.
Aplicar encoding UTF-8 para evitar problemas con tildes y caracteres especiales.
'''
df['ESTABLECIMIENTO'] = df['ESTABLECIMIENTO'].str.upper()
df['ESTABLECIMIENTO'] = df['ESTABLECIMIENTO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
print("Limpieza de ESTABLECIMIENTO completada:")
print(df['ESTABLECIMIENTO'].head())

# Limpiar las direcciones
'''
Convertir a mayúsculas para uniformidad.
Normalizar abreviaturas, es decir, cambiar 'AVENIDA' a 'AV.'
Aplicar encoding UTF-8 para consistencia con caracteres especiales.
'''
df['DIRECCION'] = df['DIRECCION'].str.upper()
df['DIRECCION'] = df['DIRECCION'].str.replace('AVENIDA', 'AV.')
df['DIRECCION'] = df['DIRECCION'].str.replace('CALLE', 'C.')
df['DIRECCION'] = df['DIRECCION'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
print("Limpieza de DIRECCION completada:")
print(df['DIRECCION'].head())

# Limpiar los valores de Supervisor y Director
'''
Convertir a mayúsculas para uniformidad.
Reemplazar valores nulos por "NO CONOCIDO".
'''
df['SUPERVISOR'] = df['SUPERVISOR'].str.upper().fillna('NO CONOCIDO')
df['DIRECTOR'] = df['DIRECTOR'].str.upper().fillna('NO CONOCIDO')
print("Limpieza de SUPERVISOR y DIRECTOR completada:")
print(df[['SUPERVISOR', 'DIRECTOR']].head())

# Llenar valores nulos en las columnas DISTRITO y DIRECCION
'''
Reemplazar valores nulos en DISTRITO y DIRECCION por "NO DISPONIBLE"
'''
df['DISTRITO'] = df['DISTRITO'].fillna('NO DISPONIBLE')
df['DIRECCION'] = df['DIRECCION'].fillna('NO DISPONIBLE')

# Remover columnas innecesarias
'''
Remover columna NIVEL ya que solo contiene un valor y no es necesaria.
'''
df.drop(columns=['NIVEL'], inplace=True, axis=1)

# Remover filas completamente vacías (por si quedaron después de la limpieza)
'''
Remover filas completamente vacías.
'''
df.dropna(how="all", inplace=True)

# Guardar el DataFrame limpio en un archivo CSV
'''
Guardar el DataFrame limpio en un archivo CSV llamado 'DEPARTAMENTOS.csv'.
'''
df.to_csv('DEPARTAMENTOS.csv', index=False)

# Limpieza finalizada, liberar memoria
'''
Liberar memoria eliminando objetos temporales.
'''
del raw_dfs
del df

print("Proceso de limpieza completado y datos guardados en 'DEPARTAMENTOS.csv'")
