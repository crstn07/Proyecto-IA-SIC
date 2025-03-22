from flask import Flask, jsonify, request
from flask_cors import CORS
from chat import get_recommendations
print("Hola mundo")
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def prueba():
    return jsonify({"mensaje": "Hola mundo"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # {"query": "Quiero ver una película de acción"}
        query = request.json['query']
        recomendaciones = get_recommendations(query)
        return jsonify({"recomendaciones": recomendaciones})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)