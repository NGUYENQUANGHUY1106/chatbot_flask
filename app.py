from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os  

app = Flask(__name__)
CORS(app)

# ✅ Lấy API key từ biến môi trường (Render sẽ truyền key này vào)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  

@app.route("/")
def home():
    return "✅ Chatbot Flask đang hoạt động!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
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

        # ✅ Gửi request tới OpenAI và xử lý lỗi nếu có
        response = requests.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)
        response.raise_for_status()  # Nếu OpenAI trả về lỗi → sẽ raise exception

        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Lỗi khi gọi OpenAI:", e)
        return jsonify({"reply": "⚠️ Xin lỗi, hệ thống đang gặp sự cố. Vui lòng thử lại sau!"}), 500

@app.route("/web")
def chatbot_page():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
