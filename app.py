from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = "sk-..."  # Thay bằng API key của bạn

@app.route("/")
def home():
    return "✅ Chatbot Flask đang hoạt động!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }

    res = requests.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)
    reply = res.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

@app.route("/web")
def chatbot_page():
    return render_template("index.html")