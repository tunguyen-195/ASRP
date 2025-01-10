from flask import render_template, Blueprint
from . import main_bp

@main_bp.route('/')
def index():
    return render_template('main/index.html')
