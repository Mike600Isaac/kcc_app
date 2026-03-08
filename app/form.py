from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField,PasswordField,SubmitField,TelField,TextAreaField,RadioField
from wtforms.validators import DataRequired,Email, EqualTo,Length
from flask_wtf.file import FileAllowed, FileField



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

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    

class GalleryForm(FlaskForm):
    gallery_type = SelectField("Gallery Type",
    choices=[
        ("Photo", "Photo"),
        ("Video", "Video"),
        ("Audio", "Audio"),
        ("Document", "Document")
        ],validators=[DataRequired()])
    title = StringField("Title / Caption",validators=[DataRequired()])
    ministry = SelectField("Ministry",
        choices=[
            ("", "Select Ministry"),
            ("Children Ministry", "Children Ministry"),
            ("Youth Ministry", "Youth Ministry"),
            ("Campus Ministry", "Campus Ministry"),
            ("Young Adult Ministry", "Young Adult Ministry"),
            ("Women Ministry", "Women Ministry")
        ]
    )
    file = FileField(
        "Upload File",
        validators=[
            DataRequired(),
            FileAllowed(
                ["jpg","png","jpeg","mp4","mp3","pdf","docx"],
                "Invalid file type"
            )
        ]
    )   
    description = TextAreaField("Description")
    submit = SubmitField("Add to Gallery")
