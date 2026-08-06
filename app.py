from flask import Flask, request
from google import genai

app = Flask(__name__)

client = genai.Client(api_key="")

@app.route('/')
def home():
    return "Cerelumen AI Backend is running successfully!"

@app.route('/api/analyze', methods=['POST'])
def analyze_patient():
    raw_data = request.data.decode('utf-8')
    print("Received data:", raw_data)
    
    parts = raw_data.split(',')
    
    if len(parts) >= 6:
        age = parts[0].strip()
        gender = parts[1].strip()
        family_history = parts[2].strip()
        apoe4 = parts[3].strip()
        diet_pattern = parts[4].strip()
        physical_activity = parts[5].strip()
    else:
        age, gender, family_history, apoe4, diet_pattern, physical_activity = [p.strip() for p in (parts + ["غير متوفر"] * 6)[:6]]

    prompt = f"بناءً على بيانات المريض: العمر {age}، الجنس {gender}، التاريخ العائلي {family_history}، جينات apoe4 {apoe4}، نمط الغذاء {diet_pattern}، والنشاط البدني {physical_activity}، قم بتحليل الحالة."
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    
    return response.text

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)   