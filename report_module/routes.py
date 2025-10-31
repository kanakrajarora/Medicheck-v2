from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from . import report_bp

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages)
    return text.strip()

def analyze_medical_report(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    prompt = f"Summarize this medical report in ~100 words:\n{text}"
    response = model.generate_content(prompt)
    return response.text

def send_report_email(to_email, summary_text):
    sender_email = os.getenv("EMAIL_USER", "yourmail@gmail.com")
    sender_password = os.getenv("EMAIL_PASS", "yourapppassword")
    subject = "Your Medical Report Summary"
    msg = MIMEMultipart("alternative")
    msg['From'], msg['To'], msg['Subject'] = sender_email, to_email, subject
    msg.attach(MIMEText(summary_text, 'html'))
    server = smtplib.SMTP('smtp.mailersend.net', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()

@report_bp.route('/')
def report_home():
    return render_template("index.html")

@report_bp.route('/analyze-report', methods=['POST'])
def analyze_report():
    if 'report' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['report']
    email = request.form.get('email', '').strip()
    send_email_flag = request.form.get('sendEmail') == 'true'
    if not file.filename:
        return jsonify({"error": "Empty file name"}), 400

    upload_path = os.path.join("uploads", secure_filename(file.filename))
    os.makedirs("uploads", exist_ok=True)
    file.save(upload_path)

    insights = analyze_medical_report(upload_path)
    if send_email_flag and email:
        send_report_email(email, insights)

    return jsonify({"summary": insights})
