from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TelField,TextAreaField,RadioField
from wtforms.validators import DataRequired,Email,Length



class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = TelField("Phone Number", validators=[DataRequired(), Length(min=5, max=20)])
    message = TextAreaField('Message', validators=[DataRequired()])
    contact_method = RadioField('Preferred Contact Method',choices=[('call', 'Call'), ('text', 'Text')],validators=[DataRequired()])
    submit = SubmitField('Submit')

class AdminLoginForm(FlaskForm):
    email = StringField('Admin Email',validators=[DataRequired(message="Email is required"),Email(message="Enter a valid email")])
    password = PasswordField('Password',validators=[DataRequired(message="Password is required"),Length(min=6, message="Password must be at least 6 characters")])
    submit = SubmitField('Login')
