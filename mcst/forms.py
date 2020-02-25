from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField,  RadioField, BooleanField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_project.models import User


class convid_declaration(FlaskForm):
    choices = [(1, 'YES'), (0, 'NO')]
    full_name = StringField('full_name ', validators=[DataRequired()])
    contact_no =StringField('contact_no ',validators=[DataRequired()])
    date_registered = DateField('date_registered ', format= '%Y-%m-%d')
    unit_visted = StringField('unit_visted ',validators=[DataRequired()])
    nric = StringField('NRIC last 4 characters',validators=[DataRequired(), Length(4)])
    mainland_visit = RadioField('mainland_visit',validators=[], choices= choices, default="0", coerce=int)
    family_visit =RadioField('family_visit',validators=[], choices= choices, default="0", coerce=int)
    fever =RadioField('fever',validators=[], choices= choices, default="0", coerce=int)
    respiratory = RadioField('respiratory',validators=[], choices= choices, default="0", coerce=int)
    contact_convid =RadioField('contact_convid',validators=[], choices= choices, default="0", coerce=int)
    # contact_place = StringField('declaration',validators=[DataRequired()])
    declaration =BooleanField('contact_place',validators=[DataRequired()])

    submit = SubmitField('Submit Declaration')


class Upload_pending_docs(FlaskForm):

    item_id = StringField('item ',
                           validators=[DataRequired()])
    item = StringField('item ',
                           validators=[DataRequired()])
    File_uploaded = FileField('File_uploaded ')
    submit = SubmitField('Upload')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('That username is taken. Please choose a different one.')
    #
    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That email is taken. Please choose a different one.')

class Audit_breakdown_item(FlaskForm):

    item_id = StringField('item ',
                           validators=[DataRequired()])
    item = StringField('item ',
                           validators=[DataRequired()])
    File_uploaded = FileField('File_uploaded ')
    submit = SubmitField('Upload')

class TemperatureForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    Temperature = StringField('Temperature', validators=[Length(min=4 , max= 4)])
    submit = SubmitField('Input Temperature')
    delete = SubmitField('Delete Entry')
