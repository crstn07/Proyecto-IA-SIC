import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from chatterbot import ChatBot
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

# ======================
# CARGA Y PREPROCESAMIENTO
# ======================
# Cargar el dataset (asegúrate de que 'peliculas.csv' esté en el mismo directorio)
df = pd.read_csv('peliculas.csv')

# Rellenar valores faltantes en las columnas relevantes
for col in ['Género', 'Sinopsis', 'Director', 'Elenco', 'País', 'Tipo', 'Clasificación', 'Plataforma']:
    df[col] = df[col].fillna('')

# Crear una columna combinada con la información clave en minúsculas
df['combined'] = (
    df['Género'] + ' ' +
    df['Sinopsis'] + ' ' +
    df['Director'] + ' ' +
    df['Elenco'] + ' ' +
    df['País'] + ' ' +
    df['Tipo'] + ' ' +
    df['Clasificación'] + ' ' +
    df['Plataforma']
).str.lower()

# Inicializar el vectorizador TF-IDF usando stop words en español
vectorizer = TfidfVectorizer(stop_words='spanish')
tfidf_matrix = vectorizer.fit_transform(df['combined'])

# ======================
# FUNCIÓN DE RECOMENDACIÓN
# ======================
def get_recommendations(query, top_n=5):
    """
    Recibe una consulta en texto libre, la vectoriza y calcula la similitud del coseno con
    cada película para retornar las top_n recomendaciones.
    """
    query = query.lower().strip()
    query_vec = vectorizer.transform([query])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = cosine_sim.argsort()[-top_n:][::-1]
    recommendations = df.iloc[top_indices].copy()
    recommendations['score'] = cosine_sim[top_indices]
    return recommendations

# ======================
# ADAPTADOR PERSONALIZADO CON CHATTERBOT
# ======================
class MovieRecommendationAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
    
    def can_process(self, statement):
        # En este ejemplo, procesamos todas las entradas.
        return True

    def process(self, statement, additional_response_selection_parameters):
        # Utiliza el texto ingresado para obtener recomendaciones
        recommendations = get_recommendations(statement.text, top_n=5)
        if recommendations.empty:
            response_text = "Lo siento, no encontré películas que se ajusten a tu consulta."
        else:
            response_text = "Te recomiendo las siguientes películas:\n"
            for idx, row in recommendations.iterrows():
                response_text += f"- {row['Título']} ({row['Año de lanzamiento']}) en {row['Plataforma']}\n"
        response_statement = Statement(text=response_text)
        response_statement.confidence = 1
        return response_statement

# ======================
# CONFIGURACIÓN DEL CHATBOT CON CHATTERBOT
# ======================
chatbot = ChatBot(
    "MovieBot",
    logic_adapters=[
        {
            "import_path": "__main__.MovieRecommendationAdapter"
        }
    ]
)

# ======================
# BUCLE INTERACTIVO
# ======================
print("Hola, soy MovieBot. Pregunta por una recomendación de película o escribe 'salir' para terminar.")
while True:
    try:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            print("¡Hasta luego!")
            break
        response = chatbot.get_response(user_input)
        print("MovieBot:", response.text)
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
