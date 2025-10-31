from flask import request, jsonify, render_template
from . import disease_bp
import pandas as pd
import numpy as np
from .model import preprocess_symptoms, load_model
from pymongo import MongoClient
from datetime import datetime
from urllib.parse import quote_plus
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------------------- Mongo Connection ----------------------------
username = quote_plus("admin")
password = quote_plus("admin@1234")
mongo_url = f"mongodb+srv://{username}:{password}@medicheck.n8i0hmp.mongodb.net/"
client = MongoClient(mongo_url)
db = client['disease_prediction_db']
collection = db['predictions']

model, scaler, symptom_columns = load_model()

@disease_bp.route('/')
def disease_home():
    return render_template('index1.html')

@disease_bp.route('/predict-disease', methods=['POST'])
def predict_disease():
    data = request.json
    symptoms = data.get('symptoms', [])
    email = data.get('email', '')
    send_email_flag = data.get('sendEmail', False)

    input_data = preprocess_symptoms(symptoms, symptom_columns)
    input_df = pd.DataFrame([input_data], columns=symptom_columns)
    probabilities = model.predict_proba(input_df) * 100
    top_2_indices = np.argsort(probabilities[0])[-2:][::-1]
    top_2_diseases = model.classes_[top_2_indices]
    top_2_probabilities = probabilities[0][top_2_indices]

    record = {
        "input_symptoms": symptoms,
        "processed_input": input_data.tolist(),
        "top_predictions": [
            {"disease": top_2_diseases[0], "probability": float(top_2_probabilities[0])},
            {"disease": top_2_diseases[1], "probability": float(top_2_probabilities[1])}
        ],
        "timestamp": datetime.now()
    }
    collection.insert_one(record)

    if send_email_flag and email:
        try:
            send_prediction_email(email, symptoms, top_2_diseases, top_2_probabilities)
        except Exception as e:
            print(f"Error sending email: {e}")

    return jsonify({
        'diseases': top_2_diseases.tolist(),
        'probabilities': top_2_probabilities.tolist()
    })

def send_prediction_email(to_email, symptoms, diseases, probabilities):
    sender_email = os.getenv("EMAIL_USER", "yourmail@gmail.com")
    sender_password = os.getenv("EMAIL_PASS", "yourapppassword")
    subject = "Your MediCheck Health Prediction Results"
    disease_rows = "".join(
        f"<tr><td>{d}</td><td>{p:.2f}%</td></tr>"
        for d, p in zip(diseases, probabilities)
    )
    body = f"<h2>MediCheck Prediction</h2><p>Symptoms: {', '.join(symptoms)}</p><table>{disease_rows}</table>"
    msg = MIMEMultipart("alternative")
    msg['From'], msg['To'], msg['Subject'] = sender_email, to_email, subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.mailersend.net', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
