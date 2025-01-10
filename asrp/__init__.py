from flask import Flask, render_template
from config import Config
from .extensions import db, migrate, login_manager
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .blueprints.report import report_bp
from .blueprints.police_officer import police_officer_bp
import logging
from logging.handlers import RotatingFileHandler

# Thêm import
from flask_admin import Admin
from .admin_views import AdminModelView, CustomAdminIndexView  # Tệp chứa lớp AdminModelView đã custom
from .models import User, Report, Area, Unit  # Import các model cần quản trị

def setup_logging(app):
    """
    Thiết lập logging cho ứng dụng.
    """
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=5)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler.setFormatter(formatter)
    
    # Ghi log ra console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.addHandler(console_handler)

def create_app(config_class=Config):
    """
    Tạo Flask app với các cấu hình, blueprint, và tích hợp Flask-Admin.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Cấu hình logging
    logging.basicConfig(level=logging.DEBUG,  # Thay đổi mức độ logging nếu cần
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.StreamHandler()])

    # Khởi tạo các thành phần mở rộng
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Thiết lập logging
    setup_logging(app)

    # Đăng ký blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(police_officer_bp, url_prefix='/police_officer')

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Khởi tạo Flask-Admin
    admin = Admin(
        app,
        name="ASRP Admin",
        template_mode='bootstrap4',
        url="/admin",
        index_view=CustomAdminIndexView()  # Sử dụng lớp CustomAdminIndexView
    )

    # Đăng ký các model với Flask-Admin
    with app.app_context():
        db.create_all()  # Nếu không dùng flask-migrate, giữ dòng này để tạo bảng
        # Đăng ký các model với Flask-Admin, sử dụng endpoint duy nhất
        admin.add_view(AdminModelView(User, db.session, endpoint='admin_user'))
        admin.add_view(AdminModelView(Report, db.session, endpoint='admin_report'))
        admin.add_view(AdminModelView(Area, db.session, endpoint='admin_area'))
        admin.add_view(AdminModelView(Unit, db.session, endpoint='admin_unit'))

    # Xử lý lỗi 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
