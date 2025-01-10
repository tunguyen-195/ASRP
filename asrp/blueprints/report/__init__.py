from flask import Blueprint

report_bp = Blueprint('report', __name__, url_prefix='/reports')

from . import routes
