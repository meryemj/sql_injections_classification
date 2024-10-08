from flask import Flask, request, jsonify
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Charger le modèle LSTM
model_lstm = load_model('lstm_model.h5')

# Charger le tokenizer
with open("C:/Users/merye/OneDrive/Documents/tokenizer.pkl", 'rb') as handle:
    tokenizer = pickle.load(handle)

# Initialiser l'application Flask
app = Flask(__name__)

# Fonction de prédiction
def predict_sql_injection(query, threshold=0.5):
    # Tokenizer et pad la nouvelle requête
    sequence = tokenizer.texts_to_sequences([query])
    padded_sequence = pad_sequences(sequence, maxlen=100)
    
    # Faire la prédiction avec le modèle LSTM
    prediction = model_lstm.predict(padded_sequence)[0][0]
    
    # Appliquer un seuil pour déterminer si c'est une injection SQL
    if prediction > threshold:
        result = 'SQL Injection'
    else:
        result = 'Normal Query'
    
    return {"prediction_probability": float(prediction), "classification": result}



@app.route('/')
def home():
    return "Hello, Welcome to SQL Injections Classification Page"


# Route pour prédire une requête SQL
@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données JSON envoyées par la requête
    data = request.get_json(force=True)
    
    # Extraire la requête SQL de la requête
    query = data.get('query')
    
    if query:
        # Effectuer la prédiction
        result = predict_sql_injection(query)
        return jsonify(result)
    else:
        return jsonify({"error": "No query provided"}), 400

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
