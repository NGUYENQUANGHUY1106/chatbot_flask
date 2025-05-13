from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Lấy API key từ biến môi trường
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Kiểm tra API key có tồn tại không
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY chưa được thiết lập. Vui lòng kiểm tra biến môi trường trên Render.")

@app.route("/")
def home():
    return "✅ Chatbot Flask đang hoạt động!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    print("📩 Tin nhắn người dùng:", user_message)
    print("🔑 API Key (ẩn bớt):", OPENAI_API_KEY[:10] + "..." if OPENAI_API_KEY else "Không có")

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
        print("📨 Raw Response:", res.text)

        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Exception:", str(e))
        print("📩 Nội dung trả về:", res.text if 'res' in locals() else "Không có phản hồi từ OpenAI")
        return jsonify({"reply": "⚠️ Hệ thống gặp lỗi khi kết nối đến AI."}), 500

@app.route("/web")
def chatbot_page():
    return render_template("index.html")

# Route kiểm tra key nếu cần debug
@app.route("/check-key")
def check_key():
    return f"🔍 API Key: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "❌ API key không tồn tại!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
