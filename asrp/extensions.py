from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = 'auth.dang_nhap'  # Tên route của trang đăng nhập
login_manager.login_message = "Vui lòng đăng nhập trước."

