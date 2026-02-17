from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Trang chủ của chatbot
@app.route('/')
def index():
    return render_template('index.html')

# Xử lý tin nhắn từ người dùng
@app.route('/get_response', methods=['POST'])
def get_response():
    user_text = request.json.get("msg").lower()
    
    # Logic trả lời của bot
    if "xin chào" in user_text:
        return jsonify({"reply": "Chào bạn! Chúc bạn một ngày tốt lành."})
    elif "thời tiết" in user_text:
        return jsonify({"reply": "Hôm nay trời đẹp để học lập trình đó!"})
    elif "ai tạo ra bạn" in user_text:
        return jsonify({"reply": "Tôi được tạo ra bởi một lập trình viên tương lai là bạn đấy!"})
    else:
        return jsonify({"reply": "Xin lỗi, tôi chưa hiểu ý bạn. Thử hỏi 'Xin chào' xem?"})

if __name__ == "__main__":
    app.run(debug=True)