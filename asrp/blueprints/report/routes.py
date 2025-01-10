from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import report_bp
from .forms import ReportForm
from ...extensions import db
from ...models import Report, Attachment

@report_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_report():
    form = ReportForm()
    if form.validate_on_submit():
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            report = Report(
                title=form.title.data,
                description=form.description.data,
                latitude=form.latitude.data,
                longitude=form.longitude.data,
                area_id=form.area_id.data,
                user_id=current_user.id,
                assigned_officer_id=form.assigned_officer_id.data if form.assigned_officer_id.data != 0 else None
            )
            db.session.add(report)
            db.session.commit()

            report_folder = os.path.join(upload_folder, f'report_{report.id}')
            if not os.path.exists(report_folder):
                os.makedirs(report_folder)

            for file in form.attachments.data:
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(report_folder, filename)
                    file.save(file_path)

                    attachment = Attachment(
                        report_id=report.id,
                        file_path=file_path,
                        file_type=file.content_type.split('/')[0],
                        file_name=filename
                    )
                    db.session.add(attachment)

            db.session.commit()

            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(success=True, message='Báo cáo đã được gửi thành công!')
            else:
                flash('Báo cáo đã được gửi thành công!', 'success')
                return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(success=False, message=str(e)), 500
            else:
                flash('Đã xảy ra lỗi khi gửi báo cáo. Vui lòng thử lại.', 'error')
                return redirect(url_for('report.submit_report'))

    return render_template('report/submit_report.html', form=form)

@report_bp.route('/<int:report_id>')
@login_required
def report_detail(report_id):
    rep = Report.query.get_or_404(report_id)
    return render_template('report/report_detail.html', report=rep)
