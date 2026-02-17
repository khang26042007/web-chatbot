import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 1. Cấu hình API Key (Thay mã của bạn vào đây)
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Khởi tạo mô hình Gemini
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_message = request.json.get("msg")
        
        if not user_message:
            return jsonify({"reply": "Bạn chưa nhập gì cả..."})

        # 3. Gửi câu hỏi đến Gemini AI
        response = model.generate_content(user_message)
        
        # Lấy văn bản phản hồi từ AI
        bot_reply = response.text
        
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Lỗi: {e}")
        return jsonify({"reply": "Hệ thống AI đang bận, bạn thử lại sau nhé!"})

if __name__ == "__main__":
    app.run(debug=True)