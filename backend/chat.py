#pip install -r requirements.txt
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
df = pd.read_csv('../data/dataset.csv')

#convertir la columna year a string
df['year'] = df['year'].astype(str)
df.fillna('', inplace=True)

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
    return recommendations

# ======================
# Chatbot simple
# ======================
def chatbot():
    print("Ingresa tu consulta en lenguaje natural o escribe 'salir' para terminar.")
    
    while True:
        query = input("\nTu consulta: ")
        if query.lower() == 'salir':
            print("¡Hasta luego!")
            break
        
        recommendations = get_recommendations(query, top_n=5)
        if recommendations.empty:
            print("Lo siento, no se encontraron resultados para tu consulta.")
        else:
            print("\nTe recomendamos las siguientes películas/shows:")
            for idx, row in recommendations.iterrows():
                print(f"Título: {row['name']}")
                print(f"Tipo: {row['tipo']}")
                print(f"Año de lanzamiento: {row['year']}")
                print(f"Director: {row['director']}")
                print(f"Elenco: {row['elenco']}")
                print(f"País: {row['pais']}")
                print(f"Clasificación: {row['clasificacion']}")
                print(f"Duración: {row['duration']}")
                print(f"Género: {row['genero']}")
                print(f"Plataforma: {row['plataforma']}")
                print(f"Sinopsis: {row['sinopsis']}")
                print("-" * 80)
    print("Fin del chat.")

if __name__ == "__main__":
    chatbot()
