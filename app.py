import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def home():
    return "Cerelumen AI Backend is running successfully!"

@app.route('/api/analyze', methods=['POST'])
def analyze_patient():
    try:
        # فحص إذا كانت البيانات مرسلة بصيغة JSON أو نص خام
        if request.is_json:
            data = request.get_json()
            raw_data = str(data)
        else:
            raw_data = request.data.decode('utf-8')
            
        print("Received data:", raw_data)
        
        # إذا كانت البيانات فاضية تماماً، نحاول ناخذ الـ Form Data
        if not raw_data or raw_data.strip() == "":
            raw_data = request.form.get("text", "")
            
        if not raw_data or raw_data.strip() == "":
            return jsonify({"error": "No data received"}), 400

        # استدعاء نموذج جيميني للتحليل
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze the following clinical data and provide recommendations: {raw_data}"
        )
        
        return jsonify({
            "status": "success",
            "recommendation": response.text
        })
        
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
