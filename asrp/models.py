from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(
        db.Enum('user', 'police_officer', 'admin'),
        default='user',
        nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    personal_photo = db.Column(db.String(200), nullable=True)
    id_card_photo = db.Column(db.String(200), nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    verification_status = db.Column(
        db.Enum('pending', 'verified', 'rejected'),
        default='pending',
        nullable=False
    )

    # Specify the back_populates for the user-reports relationship
    reports = relationship('Report', foreign_keys='Report.user_id', back_populates='user')

    # (User -> Unit) : n user -> 1 unit => user.unit
    unit = db.relationship('Unit', backref='members', lazy='joined')

    # (User -> Content) : 1 user => n content => user.authored_contents
    authored_contents = db.relationship('Content', backref='author', lazy='dynamic')

    # (User -> UserArea) : n-n, Trung gian => user.user_areas
    # => Bên UserArea => user = relationship('User', backref='user_areas')
    # => => Tức user.user_areas
    # => => Ở đây ta không cần khai báo thêm. Backref đã xử lý
    # => => Optional: "user_area_links = db.relationship('UserArea', ...)" 
    # => => Thường ta bỏ, để không trùng
    # => => => Xem class UserArea

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # => user.members => do backref='members'

class Area(db.Model):
    __tablename__ = 'areas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # (Area -> Report) 1-n => area.reports
    # => Bên Report => area= relationship('Area', backref='reports')
    # => Ta không cần backref ở đây => "reports = db.relationship('Report', lazy='dynamic')" => optional
    # => Ko backref => tránh conflict
    # => Dùng side "Report" = backref='reports'
    # => Tức area.reports

    # (Area -> UserArea) 1-n => area.user_areas
    # => Bên UserArea => area= relationship('Area', backref='user_areas')
    # => Tức area.user_areas
    # => Ko cần define relationship here => optional
    # => Done => Ko define => SẼ TỐT HƠN => Tránh conflict
    # => => Kết luận: ta có thể BỎ hết => rely on backref from "UserArea.area"

class UserArea(db.Model):
    __tablename__ = 'user_areas'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)

    # Quan hệ (UserArea -> User)
    # => user.user_areas
    user = db.relationship('User', backref='user_areas')

    # Quan hệ (UserArea -> Area)
    # => area.user_areas
    area = db.relationship('Area', backref='user_areas')

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(
        db.Enum('new', 'in_progress', 'closed', 'resolved'),
        default='new',
        nullable=False
    )
    assigned_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Specify the foreign key for the user relationship
    user = relationship('User', foreign_keys=[user_id], back_populates='reports')

    # (Report -> assigned_officer) => "report.assigned_officer"
    assigned_officer = db.relationship('User', foreign_keys=[assigned_officer_id])

    # (Report -> Area) => 1-n => area.reports
    area = db.relationship(
        'Area',
        backref='reports', 
        lazy='joined'
    )

    # attachments => (1-n)
    attachments = db.relationship('Attachment', backref='report', lazy='select')

class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    file_type = db.Column(
        db.Enum('image','video','document','audio','other'),
        nullable=False
    )
    file_name = db.Column(db.String(200), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # => Bên Report => "attachments = db.relationship('Attachment', backref='report')"

class Content(db.Model):
    __tablename__ = 'contents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    # => "user.authored_contents" via backref='author'

class LeakedInfo(db.Model):
    __tablename__ = 'leaked_info'

    id = db.Column(db.Integer, primary_key=True)
    contact_info = db.Column(db.String(150), unique=True, nullable=False)
    info_type = db.Column(db.Enum('email', 'phone'), nullable=False)
