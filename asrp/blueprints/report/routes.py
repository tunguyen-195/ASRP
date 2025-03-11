from flask import render_template, redirect, url_for, flash, request, current_app, jsonify, send_file, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename, safe_join
import os
from . import report_bp
from .forms import ReportForm
from ...extensions import db
from ...models import Report, Attachment
from asrpbnbot import send_telegram_message  # Import the function
from sqlalchemy import func
import pandas as pd
from io import BytesIO
import logging

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
            logging.info(f"Attempting to add report: {report}")
            db.session.add(report)
            db.session.commit()
            logging.info(f"Report added with ID: {report.id}")

            report_folder = os.path.join(upload_folder, f'report_{report.id}')
            if not os.path.exists(report_folder):
                os.makedirs(report_folder)
                logging.info(f"Created folder for report ID {report.id}: {report_folder}")

            for file in form.attachments.data:
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(report_folder, filename)
                    try:
                        file.save(file_path)
                        logging.info(f"Saved file {filename} to {file_path}")

                        attachment = Attachment(
                            report_id=report.id,
                            file_path=file_path,
                            file_type=file.content_type.split('/')[0],
                            file_name=filename
                        )
                        db.session.add(attachment)
                    except Exception as e:
                        logging.error(f"Error saving file {filename}: {e}")

            try:
                db.session.commit()
                logging.info(f"Attachments added for report ID: {report.id}")
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error committing attachments for report ID {report.id}: {e}")

            # Send a notification to Telegram
            if report.latitude and report.longitude:
                location_info = f"Location: {report.latitude}, {report.longitude}\n"
                maps_link = f"[View on Google Maps](https://www.google.com/maps/search/?api=1&query={report.latitude},{report.longitude})"
            else:
                location_info = "Người báo cáo không cung cấp vị trítrí"
                maps_link = ""

            message = (
                f"🔔 *New Report Submitted*\n"
                f"Title: {report.title}\n"
                f"Description: {report.description}\n"
                f"Submitted by: {current_user.full_name} ({current_user.email})\n"
                f"Phone: {current_user.phone_number}\n"
                f"Area: {report.area.name}\n"
                f"{location_info}\n"
                f"{maps_link}\n"
                f"Date: {report.date_submitted.strftime('%d/%m/%Y %H:%M:%S')}"
            )
            send_telegram_message(message)

            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(success=True, message='Báo cáo đã được gửi thành công!')
            else:
                flash('Báo cáo đã được gửi thành công!', 'success')
                return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            logging.error(f"Error during report submission: {e}")
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

@report_bp.route('/statistics', methods=['GET', 'POST'])
@login_required
def report_statistics():
    # Fetch reports and apply filters if any
    query = Report.query

    # Apply filters based on request arguments
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        status = request.form.get('status')

        if start_date:
            query = query.filter(Report.date_submitted >= start_date)
        if end_date:
            query = query.filter(Report.date_submitted <= end_date)
        if status:
            query = query.filter(Report.status == status)

    reports = query.all()

    # Calculate statistics
    total_reports = len(reports)
    reports_by_status = db.session.query(Report.status, func.count(Report.id)).group_by(Report.status).all()

    return render_template('report/statistics.html', reports=reports, total_reports=total_reports, reports_by_status=reports_by_status)

@report_bp.route('/export_reports', methods=['POST'])
@login_required
def export_reports():
    # Fetch reports based on filters
    query = Report.query
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    status = request.form.get('status')

    if start_date:
        query = query.filter(Report.date_submitted >= start_date)
    if end_date:
        query = query.filter(Report.date_submitted <= end_date)
    if status:
        query = query.filter(Report.status == status)

    reports = query.all()

    # Log the number of reports fetched
    logging.info(f"Number of reports fetched: {len(reports)}")

    # Create a DataFrame
    data = [{
        'Title': report.title,
        'Description': report.description,
        'Status': report.status,
        'Date Submitted': report.date_submitted.strftime('%Y-%m-%d %H:%M:%S'),
        'Area': report.area.name,
        'User': report.user.full_name
    } for report in reports]

    # Log the data being written to the DataFrame
    logging.info(f"Data being written to Excel: {data}")

    df = pd.DataFrame(data)

    # Export to Excel
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Reports')
    writer.close()
    output.seek(0)

    return send_file(output, download_name='reports.xlsx', as_attachment=True)

@report_bp.route('/attachments/<int:report_id>/<filename>')
@login_required
def download_attachment(report_id, filename):
    # Construct the path to the report's folder
    report_folder = safe_join(current_app.config['UPLOAD_FOLDER'], f'report_{report_id}')
    # Serve the file from the directory
    return send_from_directory(report_folder, filename)

@report_bp.route('/my_reports', methods=['GET'])
@login_required
def my_reports():
    # Query reports submitted by the current user
    user_reports = Report.query.filter_by(user_id=current_user.id).all()
    return render_template('report/my_reports.html', reports=user_reports)
