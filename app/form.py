from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField,PasswordField,SubmitField,TelField,TextAreaField,RadioField
from wtforms.validators import DataRequired,Email, EqualTo,Length
from wtforms.fields import DateTimeLocalField  # ✅ new in WTForms ≥3
from flask_wtf.file import FileAllowed, FileField, MultipleFileField

from app.config_helpers import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, file_size_limit




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
    

class UpdateEventForm(FlaskForm):

    title = StringField(
        "Event Title",
        validators=[DataRequired(message="Event title is required")]
    )

    ministry = SelectField(
        "Ministry",
        choices=[
            ("", "Select Ministry"),
            ("Entire Church", "Entire Church"),
            ("Children Ministry", "Children Ministry"),
            ("Youth Ministry", "Youth Ministry"),
            ("Campus Ministry", "Campus Ministry"),
            ("Corper Ministry", "Corper Ministry"),
            ("Young Adult Ministry", "Young Adult Ministry"),
            ("Women Ministry", "Women Ministry"),
            ("Choir Ministry", "Choir Ministry"),
            ("Media/Electronic Ministry", "Media/Electronic Ministry")
        ],
        validators=[DataRequired(message="Please select a ministry")]
    )
    venue = StringField("Venue", validators=[DataRequired(message="Venue is required")])
    # time = StringField("Time", validators=[DataRequired(message="Time is required")])
    time = DateTimeLocalField(
    "Date & Time (Nigeria Time)",
    format="%Y-%m-%dT%H:%M",
    validators=[DataRequired()]
)

    files = MultipleFileField(
        "Upload Files",
        validators=[
            DataRequired(message="Please upload at least one file"),
            FileAllowed(
                list(ALLOWED_EXTENSIONS),
                "Only JPG, JPEG, PNG, WEBP, MP4, WEBM, OGG files are allowed."
            ),
            file_size_limit(MAX_FILE_SIZE)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired(message="Event description cannot be empty")]
    )

    submit = SubmitField("Update Event")

class EventForm(FlaskForm):

    title = StringField(
        "Event Title",
        validators=[DataRequired(message="Event title is required")]
    )

    ministry = SelectField(
        "Ministry",
        choices=[
            ("", "Select Ministry"),
            ("Entire Church", "Entire Church"),
            ("Children Ministry", "Children Ministry"),
            ("Youth Ministry", "Youth Ministry"),
            ("Campus Ministry", "Campus Ministry"),
            ("Corper Ministry", "Corper Ministry"),
            ("Young Adult Ministry", "Young Adult Ministry"),
            ("Women Ministry", "Women Ministry"),
            ("Choir Ministry", "Choir Ministry"),
            ("Media/Electronic Ministry", "Media/Electronic Ministry")
        ],
        validators=[DataRequired(message="Please select a ministry")]
    )
    venue = StringField("Venue", validators=[DataRequired(message="Venue is required")])
    # time = StringField("Time", validators=[DataRequired(message="Time is required")])
    time = DateTimeLocalField(
    "Date & Time (Nigeria Time)",
    format="%Y-%m-%dT%H:%M",
    validators=[DataRequired()]
)

    files = MultipleFileField(
        "Upload Files",
        validators=[
            DataRequired(message="Please upload at least one file"),
            FileAllowed(
                list(ALLOWED_EXTENSIONS),
                "Only JPG, JPEG, PNG, WEBP, MP4, WEBM, OGG files are allowed."
            ),
            file_size_limit(MAX_FILE_SIZE)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired(message="Event description cannot be empty")]
    )

    submit = SubmitField("Add to Event")

# class UpdateEventForm(FlaskForm):
#     title = StringField(
#         "Event Title",
#         validators=[DataRequired(message="Event title is required")]
#     )

#     ministry = SelectField(
#         "Ministry",
#         choices=[
#             ("", "Select Ministry"),
#             ("Children Ministry", "Children Ministry"),
#             ("Youth Ministry", "Youth Ministry"),
#             ("Campus Ministry", "Campus Ministry"),
#             ("Corper Ministry", "Corper Ministry"),
#             ("Young Adult Ministry", "Young Adult Ministry"),
#             ("Women Ministry", "Women Ministry"),
#             ("Choir Ministry", "Choir Ministry"),
#             ("Media/Electronic Ministry", "Media/Electronic Ministry")
#         ],
#         validators=[DataRequired(message="Please select a ministry.")]
#     )

#     description = TextAreaField(
#         "Description",
#         validators=[DataRequired(message="Event description cannot be empty")]
#     )

#     # Optional: new file upload to replace existing
#     files = MultipleFileField(
#         "Update Files",
#         validators=[
#             FileAllowed(
#                 list(ALLOWED_EXTENSIONS),
#                 "Only JPG, PNG, WEBP, MP4, WEBM, OGG files are allowed."
#             ),
#             file_size_limit(MAX_FILE_SIZE)
#         ]
#     )

#     submit = SubmitField("Update Event")



class MediaForm(FlaskForm):
    gallery_type = SelectField("Gallery Type",
    choices=[
        ("Photo", "Photo"),
        ("Video", "Video"),
        ("Audio", "Audio"),
        ("Document", "Document")
        ],validators=[DataRequired()])
    title = StringField("Title / Caption",validators=[DataRequired()])
    file = MultipleFileField(
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
    submit = SubmitField("Add to Media")
