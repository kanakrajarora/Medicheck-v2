# MediCheck

MediCheck is a unified Flask-based web application that combines **AI-powered disease prediction** and **medical report analysis** into a single, easy-to-use platform. It leverages trained ML models, Flask blueprints, and a clean modular architecture for efficient health diagnostics.

---

## Features

- **Disease Prediction** using ML models trained on symptom datasets.
- **Medical Report Analysis** for quick evaluation of uploaded health data.
- **Interactive Web Interface** built with Flask templates and static assets.
- **Modular Architecture** using Flask Blueprints.
- **Environment Variable Support** via `.env`.
- **CORS Enabled API** for smooth frontend-backend communication.
- **Deployed** on Render.

---

## Project Structure

```
MEDI-CHECK/
│
├── __pycache__/
│
├── disease_module/
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   └── index1.html
│   ├── __init__.py
│   ├── disease_prediction_model.pkl
│   ├── model.py
│   ├── more_extended_disease_symptoms.csv
│   ├── more_extended_disease_symptoms.json
│   ├── routes.py
│   └── scaler.pkl
│
├── report_module/
│   ├── static/
│   │   └── styles.css
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   └── routes.py
│
├── static/
│   └── images/
│
├── templates/
│   └── medicheck.html
│
├── .env
├── .gitignore
├── app.py
├── Procfile
└── requirements.txt
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kanakrajarora/Medicheck-v2.git
cd Medicheck-v2
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory:
```bash
EMAIL_USER=your_key
EMAIL_PASS=your_key
GOOGLE_API_KEY=your_key
PYTHON_VERSION=3.12.3
```

### 5. Run the Application
```bash
python app.py
```
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

##  Deployment

### 🔹 Render

**Procfile**:
```
web: gunicorn app:app
```

Ensure your `runtime.txt` contains:
```
python-3.12.3
```

Push your project to GitHub and connect it to your chosen hosting platform.

---

## Tech Stack

- **Backend:** Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript
- **ML Models:** Scikit-learn
- **Database:** MongoDB
- **Deployment:** Render

---

## Future Enhancements

- Add feedback storage (SQLite/MongoDB)
- Enable user authentication for personalized health history
- Include health analytics dashboard

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## 🧾 License
This project is licensed under the **MIT License**.

---

**Developed by Team MediCheck**
