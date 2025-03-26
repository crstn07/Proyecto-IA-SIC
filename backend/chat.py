import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

def preprocess_text(text):
    """
    Preprocesa el texto utilizando spaCy:
      - Convierte a minúsculas.
      - Realiza tokenización y lematización.
      - Elimina stopwords y tokens no alfabéticos.
    """
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

# ======================
# CARGA Y PREPROCESAMIENTO DEL DATASET
# ======================
df = pd.read_csv('../data/dataset2.csv')

#convertir la columna year a string
df['year'] = df['year'].astype(str)
df.fillna('N/A', inplace=True)

# Combinar información relevante y preprocesarla
df['combined'] = (
    df['name'] + ' ' +
    df['título'] + ' ' +
    df['genero'] + ' ' +
    df['sinopsis'] + ' ' +
    df['director'] + ' ' +
    df['elenco'] + ' ' +
    df['pais'] + ' ' +
    df['tipo'] + ' ' +
    df['clasificacion'] + ' ' +
    df['listed_in'] + ' ' +
    df['description'] + ' ' +
    df['year'] + ' ' +
    df['country'] + ' ' +
    df['type'] + ' ' +
    df['plataforma']
).str.lower()

# Preprocesar el contenido del dataset con spaCy
df['combined_processed'] = df['combined'].apply(preprocess_text)

# Inicializar el vectorizador TF-IDF usando la columna preprocesada
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['combined_processed'])

# ======================
# FUNCIÓN DE RECOMENDACIÓN
# ======================
def get_recommendations(query, top_n=5):
    """
    Preprocesa la consulta con spaCy, la vectoriza y calcula la similitud del coseno
    para retornar las top_n recomendaciones.
    """
    processed_query = preprocess_text(query)
    query_vec = vectorizer.transform([processed_query])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = cosine_sim.argsort()[-top_n:][::-1]
    recommendations = df.iloc[top_indices].copy()
    recommendations['score'] = cosine_sim[top_indices]
    txt = ""
    if recommendations.empty:
        return "No se encontraron resultados para tu consulta."
    else:
        txt= "\nTe recomendamos las siguientes películas/shows:\n"
        for idx, row in recommendations.iterrows():
            txt += (f"Título: {row['name']}\n")
            txt += (f"Tipo: {row['tipo']}\n")
            txt += (f"Año de lanzamiento: {row['year']}\n")
            txt += (f"Director: {row['director']}\n")
            txt += (f"Elenco: {row['elenco']}\n")        
            txt += (f"País: {row['pais']}\n")
            txt += (f"Clasificación: {row['clasificacion']}\n")
            txt += (f"Duración: {row['duration']}\n")
            txt += (f"Género: {row['genero']}\n")
            txt += (f"Plataforma: {row['plataforma']}\n")
            txt += (f"Sinopsis: {row['sinopsis']}\n")
            txt += (f"Enlace: {row['link']}\n")
            txt += "-"*90 + "\n"
    return txt