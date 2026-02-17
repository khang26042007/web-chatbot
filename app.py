import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Nạp biến môi trường từ file .env (chỉ có tác dụng khi chạy ở máy tính cá nhân)
load_dotenv()

app = Flask(__name__)

# 2. Lấy API Key từ hệ thống (Render hoặc file .env)
# Đảm bảo bạn đã đặt tên Key trên Render là: GEMINI_KEY
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

# Cấu hình Google AI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("CẢNH BÁO: Chưa tìm thấy GEMINI_KEY trong biến môi trường!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        # Lấy tin nhắn từ giao diện gửi lên
        data = request.get_json()
        user_message = data.get("msg")
        
        if not user_message:
            return jsonify({"reply": "Bạn chưa nhập tin nhắn mà..."})

        if not GOOGLE_API_KEY:
            return jsonify({"reply": "Lỗi: Bot chưa được lắp 'chìa khóa' API Key."})

        # 3. Gửi yêu cầu đến Gemini AI và nhận phản hồi
        response = model.generate_content(user_message)
        bot_reply = response.text
        
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Lỗi hệ thống: {e}")
        return jsonify({"reply": "Hệ thống AI đang bảo trì một chút, bạn thử lại sau nhé!"})

# 4. CẤU HÌNH PORT CHO RENDER (Cực kỳ quan trọng)
if __name__ == "__main__":
    # Render sẽ cấp một cổng (Port) ngẫu nhiên qua biến môi trường PORT
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' giúp server có thể truy cập được từ internet
    app.run(host='0.0.0.0', port=port)