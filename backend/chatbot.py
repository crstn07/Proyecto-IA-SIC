import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset
df = pd.read_csv('../data/dataset.csv')

# # Rellenar valores faltantes en todas las columnas con un string vacío
df.fillna('', inplace=True)

# for col in ['listed_in', 'description', 'director', 'elenco', 'country', 'type', 'clasificacion', 'plataforma']:
#     df[col] = df[col].fillna('')

# Crear una columna combinada que incluya información clave para la búsqueda libre
df['combined'] = (
    df['listed_in'] + ' ' +
    df['description'] + ' ' +
    df['director'] + ' ' +
    df['elenco'] + ' ' +
    df['country'] + ' ' +
    df['type'] + ' ' +
    df['clasificacion'] + ' ' +
    df['plataforma'] + ' ' +
    df['genero'] + ' ' +
    df['sinopsis'] + ' ' +
    df['pais'] + ' ' +
    df['tipo']
).str.lower()

# Inicializar el vectorizador TF-IDF sobre la columna combinada
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined'])

# Mapeo de palabras clave a nombres de columnas
filter_map = {
    'género': 'listed_in',
    'genero': 'listed_in',
    'año': 'year',
    'anio': 'year',
    'año de lanzamiento': 'year',
    'director': 'director',
    'actor': 'elenco',
    'actriz': 'elenco',
    'elenco': 'elenco',
    'sinopsis': 'description',
    'descripcion': 'description',
    'descripción': 'description',
    'trama': 'description',
    'país': 'country',
    'pais': 'country',
    'película': 'type',
    'pelicula': 'type',
    'serie': 'type',
    'show': 'type',
    'tipo': 'type',
    'clasificación': 'clasificacion',
    'clasificacion': 'clasificacion',
    'edad': 'clasificacion',
    'plataforma': 'plataforma',
    'plataformas': 'plataforma',
    'streaming': 'plataforma'
}

def parse_filters(query):
    """
    Extrae filtros del query en formato 'clave: valor' o 'clave=valor'.
    Retorna un diccionario con los filtros y el texto libre restante.
    """
    filters = {}
    # Patrón para extraer pares clave-valor (separados por ':' o '=' y separados por comas)
    pattern = r'(\w[\w\s]*\w)\s*[:=]\s*([^,]+)'
    matches = re.findall(pattern, query, re.IGNORECASE)
    
    # Remover los pares encontrados del query
    for key, value in matches:
        key_lower = key.strip().lower()
        if key_lower in filter_map:
            filters[filter_map[key_lower]] = value.strip().lower()  # se guarda en minúsculas para facilitar la comparación
        # Se elimina esta parte del query
        query = query.replace(f"{key}:{value}", "")
        query = query.replace(f"{key}={value}", "")
        
    # El texto libre restante se limpia de espacios adicionales y se pone en minúsculas
    free_text = query.strip().lower()
    return filters, free_text

def apply_filters(df, filters):
    """
    Aplica los filtros al DataFrame utilizando coincidencia insensible a mayúsculas/minúsculas.
    """
    filtered_df = df.copy()
    for col, value in filters.items():
        filtered_df = filtered_df[filtered_df[col].astype(str).str.lower().str.contains(value, na=False)]
    return filtered_df

def get_recommendations(query, top_n=5):
    """
    Procesa el query, aplica los filtros y realiza un ranking (si se provee texto libre) para
    retornar las top_n recomendaciones.
    """
    filters, free_text = parse_filters(query)
    
    # Filtrar el dataset según los filtros encontrados (si hay alguno)
    filtered_df = apply_filters(df, filters) if filters else df.copy()
    
    if filtered_df.empty:
        print("No se encontraron películas que cumplan con los filtros especificados.")
        return pd.DataFrame()
    
    # Si se proporcionó texto libre, se usa para rankear los resultados
    if free_text:
        free_text_vec = vectorizer.transform([free_text])
        similarity_scores = cosine_similarity(free_text_vec, vectorizer.transform(filtered_df['combined'])).flatten()
        filtered_df = filtered_df.copy()
        filtered_df['similarity'] = similarity_scores
        filtered_df = filtered_df.sort_values(by='similarity', ascending=False)
    else:
        # Si no hay texto libre, se ordena por año de lanzamiento de forma descendente
        filtered_df = filtered_df.sort_values(by='Año de lanzamiento', ascending=False)
    
    return filtered_df.head(top_n)

def chatbot():
    """
    Chatbot interactivo para recomendar películas/show de televisión.
    Puedes ingresar filtros en formato 'clave: valor' separados por comas,
    y también agregar texto libre para búsqueda general.
    
    Ejemplo: "género: acción, año: 2020, director: Tarantino"
    """
    print("Bienvenido al chatbot de recomendaciones de películas y shows.")
    print("Puedes consultar utilizando filtros en el siguiente formato:")
    print("  género, año (de lanzamiento), director, actor, sinopsis, país, tipo, clasificación, plataforma")
    print("Ejemplo de consulta: 'género: acción, año: 2020, director: Tarantino'")
    print("También puedes agregar texto libre para una búsqueda general.")
    print("Escribe 'salir' para terminar.")
    
    while True:
        user_query = input("\nTu consulta: ")
        if user_query.lower() == "salir":
            print("Gracias por usar el sistema de recomendaciones. ¡Hasta luego!")
            break
        
        recommendations = get_recommendations(user_query, top_n=5)
        if recommendations.empty:
            continue
        
        print("\nTe recomendamos las siguientes películas/shows:\n")
        for idx, row in recommendations.iterrows():
            print(f"Título: {row['name']}")
            print(f"Tipo: {row['tipo']}")
            print(f"Año de lanzamiento: {row['year']}")
            print(f"Director: {row['director']}")
            print(f"Elenco: {row['elenco']}")
            print(f"País: {row['pais']}")
            print(f"Clasificación: {row['clasificacion']}")
            print(f"Género: {row['genero']}")
            print(f"Plataforma: {row['plataforma']}")
            # Muestra una vista previa de la sinopsis
            print(f"Sinopsis: {row['sinopsis'][:350]}...")
            print("-" * 50)

if __name__ == "__main__":
    chatbot()
