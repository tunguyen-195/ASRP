from flask import render_template, Blueprint, flash, redirect, url_for
from . import main_bp
from ...forms import CheckInfoForm
from ...models import LeakedInfo

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/check_info', methods=['GET', 'POST'])
def check_info():
    form = CheckInfoForm()
    if form.validate_on_submit():
        contact_info = form.contact_info.data.strip()
        # Kiểm tra xem contact_info là email hay số điện thoại
        if '@' in contact_info:
            info_type = 'email'
        else:
            info_type = 'phone'
        
        # Tìm kiếm trong cơ sở dữ liệu
        leaked = LeakedInfo.query.filter_by(contact_info=contact_info, info_type=info_type).first()
        if leaked:
            flash('Số điện thoại/email của bạn đã bị lộ thông tin cá nhân, liên hệ lực lượng chức năng để nhận được thêm hỗ trợ.', 'danger')
        else:
            flash('Thông tin của bạn an toàn.', 'success')
        return redirect(url_for('main.check_info'))
    
    return render_template('main/check_info.html', form=form)
