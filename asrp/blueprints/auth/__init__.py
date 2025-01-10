from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
# auth_bp = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')

from . import routes
