from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Chargement de la clé
load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    if not openai.api_key:
        return jsonify({"reply": "Erreur: Clé API introuvable dans le fichier .env"})

    try:
        # Version OpenAI 0.28
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un guide touristique expert de la Tunisie."},
                {"role": "user", "content": user_input}
            ]
        )
        return jsonify({"reply": response.choices[0].message.content})
    
    except Exception as e:
        print(f"--- ERREUR OPENAI : {e} ---")
        return jsonify({"reply": f"Souci technique: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)