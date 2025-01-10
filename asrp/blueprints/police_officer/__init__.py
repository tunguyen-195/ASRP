from flask import Blueprint

police_officer_bp = Blueprint('police_officer', __name__, url_prefix='/police')

from . import routes
