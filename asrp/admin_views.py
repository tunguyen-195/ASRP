from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash, request
from flask_admin import AdminIndexView

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập trang này.", "danger")
        return redirect(url_for('auth.dang_nhap', next=request.url))

class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash("Bạn không có quyền truy cập trang này.", "danger")
        return redirect(url_for('auth.dang_nhap', next=request.url))
