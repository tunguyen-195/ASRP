from flask import render_template
from flask_login import login_required, current_user
from . import admin_bp

@admin_bp.route('/')
@login_required
def dashboard():
    # Giả sử trang này chỉ cho admin
    if current_user.role != 'admin':
        return "Bạn không có quyền truy cập trang admin.", 403
    return render_template('admin/dashboard.html')
