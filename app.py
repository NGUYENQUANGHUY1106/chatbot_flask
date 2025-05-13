from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Lấy API key từ biến môi trường
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

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

    try:
        res = requests.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)
        print("📦 Status Code:", res.status_code)
        print("📩 Raw Response:", res.text)

        res.raise_for_status()
        json_data = res.json()
        reply = json_data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({"reply": "⚠️ Hệ thống gặp lỗi khi kết nối đến AI."}), 500


@app.route("/web")
def chatbot_page():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
