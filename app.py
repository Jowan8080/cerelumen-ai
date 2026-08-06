import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

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

        # استخدام الموديل المعتمد والمستقر 1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"Analyze the following clinical data and provide recommendations: {data}")
        
        return jsonify({
            "status": "success",
            "recommendation": response.text
        })
        
    except Exception as e:
        return jsonify({
            "status": "success",
            "recommendation": f"خطأ: {str(e)}"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
