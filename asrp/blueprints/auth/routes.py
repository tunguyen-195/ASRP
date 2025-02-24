from flask import (
    render_template, redirect, url_for, flash, request, Blueprint
)
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import LoginForm, RegisterForm
from ...extensions import db, login_manager
from ...models import User

# Nếu bạn đã khai báo auth_bp ở nơi khác, có thể bỏ dòng này

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def dang_nhap():
    """
    Trang đăng nhập dùng chung cho mọi tác nhân (user/canh_sat/admin).
    Render animated_login.html (SVG animation), 
    nhưng vẫn xài WTForms LoginForm để kiểm tra email, password.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Đăng nhập thành công.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Thông tin đăng nhập không chính xác.', 'danger')
    
    return render_template("auth/animated_login.html", form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def dang_ky():
    """
    Trang đăng ký tài khoản. 
    Chỉ là ví dụ - tuỳ bạn mở/đóng tính năng đăng ký.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            new_user = User(
                full_name=form.full_name.data,
                email=form.email.data,
                phone_number=form.phone_number.data
            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('auth.dang_nhap'))
        except Exception as e:
            db.session.rollback()
            flash('Đã xảy ra lỗi trong quá trình đăng ký. Vui lòng thử lại.', 'danger')
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def dang_xuat():
    logout_user()
    flash('Bạn đã đăng xuất.', 'success')
    return redirect(url_for('main.index'))
