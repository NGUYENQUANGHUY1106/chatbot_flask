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

        res = requests.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)

        # In toàn bộ nội dung phản hồi nếu status code không phải 200
        if res.status_code != 200:
            print("❌ RESPONSE FROM OPENAI:", res.status_code, res.text)
            return jsonify({"reply": "⚠️ Hệ thống gặp lỗi khi kết nối đến AI."}), 500

        reply = res.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Lỗi exception:", e)
        return jsonify({"reply": "⚠️ Hệ thống gặp lỗi xử lý AI."}), 500


@app.route("/web")
def chatbot_page():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
