from flask import Blueprint

disease_bp = Blueprint('disease', __name__, 
                       template_folder='templates', 
                       static_folder='static')

from . import routes