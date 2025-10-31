import os
from flask import Flask, render_template
from flask_cors import CORS
from disease_module import disease_bp
from report_module import report_bp

# Compute the absolute path to your project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Flask with correct absolute template/static paths
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)

# Register Blueprints
app.register_blueprint(disease_bp, url_prefix="/disease")
app.register_blueprint(report_bp, url_prefix="/report")

@app.route('/')
def home():
    return render_template('medicheck.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
