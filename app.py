import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# جلب المفتاح وتكوينه مباشرة عبر مكتبة جوجل الرسمية
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

@app.route('/')
def home():
    return "Cerelumen AI Backend is running successfully!"

@app.route('/api/analyze', methods=['POST'])
def analyze_patient():
    try:
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

        # استخدام الموديل بالطريقة الرسمية الصحيحة للمكتبة
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Analyze the following clinical data and provide recommendations: {data}"
        
        response = model.generate_content(prompt)
        recommendation_text = response.text

        return jsonify({
            "status": "success",
            "recommendation": recommendation_text
        })
        
    except Exception as e:
        return jsonify({
            "status": "success",
            "recommendation": f"خطأ التقاط: {str(e)}"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
