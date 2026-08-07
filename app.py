import os
import logging
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("cerelumen")

# ---------------- Gemini Client ----------------
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else genai.Client()

MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")

# ---------------- System Instruction ----------------
SYSTEM_INSTRUCTION = """
أنت مساعد سريري (Clinical Decision Support) موجّه لأطباء المخ والأعصاب،
تساعدهم في اقتراح خطط غذائية ومكملات غذائية داعمة لمرضى في مراحل مبكرة
من الزهايمر أو معرّضين لخطر الإصابة به.

قواعد إلزامية في كل رد:
1. المخاطَب طبيب مختص وليس مريض — استخدم لغة سريرية دقيقة.
2. اذكر الأساس العلمي أو النظام الغذائي المرجعي إن وجد (مثل MIND diet،
   DASH diet، أبحاث حول أوميغا-3، فيتامين B12/D، الكركمين... إلخ)
   بدل تقديم توصية عامة بدون سند.
3. نبّه صراحة إلى أي تفاعلات دوائية محتملة مع أدوية الزهايمر الشائعة
   (مثل Donepezil، Memantine، Rivastigmine) إذا كانت ذات صلة بالمكمل المقترح.
4. إذا لم تكن المعلومات المتوفرة عن حالة المريض كافية لإعطاء توصية دقيقة،
   اذكر ذلك صراحة واطلب بيانات إضافية بدل التخمين.
5. اختم كل رد بجملة توضح أن هذه توصية مساعدة (AI-generated) ولا تُغني
   عن التقييم السريري والحكم الطبي للطبيب المعالج.
"""

DISCLAIMER = (
    "⚠️ هذه توصية مساعدة تم توليدها بواسطة الذكاء الاصطناعي، "
    "وهي أداة دعم قرار فقط ولا تُغني عن التقييم السريري والحكم "
    "الطبي للطبيب المعالج، خصوصاً فيما يخص التفاعلات الدوائية."
)


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

        logger.info(f"Incoming analyze request | data_len={len(data)}")

        prompt = (
            f"بيانات الحالة السريرية المقدَّمة من الطبيب:\n{data}\n\n"
            "بناءً على هذه البيانات، اقترح خطة غذائية ومكملات غذائية "
            "مناسبة مع ذكر الأساس العلمي والتفاعلات الدوائية المحتملة."
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            ),
        )
        recommendation_text = response.text

        logger.info("Gemini response received successfully")

        return jsonify({
            "status": "success",
            "recommendation": recommendation_text,
            "disclaimer": DISCLAIMER
        })

    except Exception as e:
        logger.exception("Error while processing /api/analyze")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
