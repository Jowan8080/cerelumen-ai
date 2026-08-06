import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Cerelumen AI Backend is running successfully!"

@app.route('/api/analyze', methods=['POST'])
def analyze_patient():
    try:
        raw_data = ""
        
        if request.data:
            try:
                raw_data = request.data.decode('utf-8')
            except:
                pass
                
        if not raw_data or raw_data.strip() == "":
            if request.form:
                raw_data = " ".join([f"{k}: {v}" for k, v in request.form.items()])
                
        if not raw_data or raw_data.strip() == "":
            raw_data = request.get_data(as_text=True)

        if not raw_data or raw_data.strip() == "":
            raw_data = "General clinical review request."

        response = model.generate_content(f"Analyze the following clinical data and provide recommendations: {raw_data}")
        
        return jsonify({
            "status": "success",
            "recommendation": response.text
        })
        
    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
