from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed
from ...models import Area, User

class ReportForm(FlaskForm):
    title = StringField('Tiêu đề báo cáo', validators=[DataRequired()])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    latitude = FloatField('Vĩ độ', validators=[Optional()])
    longitude = FloatField('Kinh độ', validators=[Optional()])
    area_id = SelectField('Khu vực', coerce=int, validators=[DataRequired()])
    assigned_officer_id = SelectField('Chỉ định trực tiếp Cán bộ Cảnh sát tiếp nhận', coerce=int, validators=[Optional()])
    attachments = MultipleFileField('Tệp đính kèm/ Dẫn chứng', validators=[
        FileAllowed(['jpg', 'png', 'pdf', 'docx', 'mp4', 'mp3'], 'Chỉ cho phép các tệp!')
    ])
    submit = SubmitField('Gửi Báo Cáo')

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.area_id.choices = [(area.id, area.name) for area in Area.query.all()]
        self.assigned_officer_id.choices = [(0, 'Không có')] + [(user.id, user.full_name) for user in User.query.filter_by(role='police_officer').all()]
