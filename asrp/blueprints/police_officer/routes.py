from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from . import police_officer_bp
from ...models import Report
from ...extensions import db
from sqlalchemy.orm import joinedload

@police_officer_bp.route('/reports', methods=['GET'])
@login_required
def view_reports():
    if current_user.role != 'police_officer':
        flash('Bạn không có quyền truy cập trang này.', 'danger')
        return redirect(url_for('main.index'))

    reports = Report.query.options(
        joinedload(Report.user),
        joinedload(Report.area),
        joinedload(Report.assigned_officer)
    ).filter(
        (Report.assigned_officer_id == None) | (Report.assigned_officer_id == current_user.id)
    ).all()

    return render_template('police_officer/reports.html', reports=reports)

@police_officer_bp.route('/reports/<int:report_id>/resolve', methods=['POST'])
@login_required
def resolve_report(report_id):
    if current_user.role != 'police_officer':
        flash('Bạn không có quyền thực hiện hành động này.', 'danger')
        return redirect(url_for('main.index'))

    report = Report.query.get_or_404(report_id)
    if report.assigned_officer_id != current_user.id:
        flash('Bạn không có quyền giải quyết báo cáo này.', 'danger')
        return redirect(url_for('police_officer.view_reports'))

    report.status = 'closed'
    db.session.commit()
    flash('Báo cáo đã được đánh dấu là đã giải quyết.', 'success')
    return redirect(url_for('police_officer.view_reports'))

@police_officer_bp.route('/reports/<int:report_id>', methods=['GET'])
@login_required
def report_detail(report_id):
    report = Report.query.options(
        joinedload(Report.user),
        joinedload(Report.attachments)
    ).get_or_404(report_id)
    
    if report.assigned_officer_id is not None and report.assigned_officer_id != current_user.id:
        flash('Bạn không có quyền xem báo cáo này.', 'danger')
        return redirect(url_for('police_officer.view_reports'))
    
    return render_template('police_officer/report_detail.html', report=report)

@police_officer_bp.route('/reports/<int:report_id>/update_status', methods=['POST'])
@login_required
def update_report_status(report_id):
    if current_user.role != 'police_officer':
        flash('Bạn không có quyền thực hiện hành động này.', 'danger')
        return redirect(url_for('main.index'))

    report = Report.query.get_or_404(report_id)
    if report.assigned_officer_id != current_user.id:
        flash('Bạn không có quyền thay đổi trạng thái báo cáo này.', 'danger')
        return redirect(url_for('police_officer.view_reports'))

    new_status = request.form.get('status')
    if new_status in ['new', 'in_progress', 'closed']:
        report.status = new_status
        db.session.commit()
        flash('Trạng thái báo cáo đã được cập nhật thành công.', 'success')
    else:
        flash('Trạng thái không hợp lệ.', 'danger')

    return redirect(request.referrer or url_for('police_officer.report_detail', report_id=report_id))
