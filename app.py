import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# إعداد المفتاح بأمان
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/')
def home():
    return "Cerelumen AI Backend is running successfully!"

@app.route('/api/analyze', methods=['POST'])
def analyze_patient():
    try:
        # استخراج البيانات بأي طريقة ترسلها التطبيق
        data = ""
        if request.is_json:
            req_json = request.get_json()
            data = str(req_json)
        elif request.form:
            data = " ".join([f"{k}: {v}" for k, v in request.form.items()])
        else:
            data = request.data.decode('utf-8', errors='ignore')
            
        if not data or data.strip() == "":
            data = "General clinical review request."

        # استخدام نموذج gemini-pro المستقر والمضمون
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"Analyze the following clinical data and provide recommendations: {data}")
        
        return jsonify({
            "status": "success",
            "recommendation": response.text
        })
        
    except Exception as e:
        # إرجاع الخطأ مباشرة إلى شاشة الجوال لنعرف المشكلة بالتحديد
        return jsonify({
            "status": "success",
            "recommendation": f"خطأ برمجي أو من المفتاح: {str(e)}"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
