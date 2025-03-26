import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv('dataset.csv')

# Crear las nuevas columnas combinadas
df['Director'] = df[['director', 'director.1']].fillna('').agg(' '.join, axis=1).str.strip()
df['Pais'] = df[['pais', 'pais.1']].fillna('').agg(' '.join, axis=1).str.strip()

# Eliminar las columnas originales
df = df.drop(columns=['director', 'director.1', 'pais', 'pais.1'])

# Asignar los valores a la nueva columna 'link' basados en la columna 'Plataforma'
df['link'] = df['plataforma'].map({
    'Disney plus': 'https://www.disneyplus.com/home',
    'Hulu': 'https://www.hulu.com/welcome',
    'Amazon Prime ': 'https://www.primevideo.com/',
    'Netflix': 'https://www.netflix.com/'
})

# Llenar valores faltantes en 'link' si es necesario
df['link'] = df['link'].fillna('Sin Link')

# Guardar el nuevo DataFrame en un archivo (opcional)
df.to_csv('dataset2.csv', index=False)
# print(df)