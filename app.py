import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

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

        # الاتصال المباشر والمضمون عبر الـ API بدون مكتبة جوجل المعقدة
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Analyze the following clinical data and provide recommendations: {data}"}]
            }]
        }

        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()

        # استخراج النص بذكاء من استجابة الـ API
        if "candidates" in res_json:
            recommendation_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            recommendation_text = str(res_json)

        return jsonify({
            "status": "success",
            "recommendation": recommendation_text
        })
        
    except Exception as e:
        return jsonify({
            "status": "success",
            "recommendation": f"خطأ: {str(e)}"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
