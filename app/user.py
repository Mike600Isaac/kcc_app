from datetime import datetime
from importlib.resources import files
import os,uuid
from flask import jsonify, render_template, request, flash, redirect, session, url_for
from app import app,csrf
from app import form
from app.form import EventForm,UpdateEventForm, MediaForm,AdminLoginForm, ResetPasswordForm,RequestResetForm
from app.models import EventFile, db,Contact,Admin,Media,Event

from werkzeug.utils import secure_filename
from functools import wraps

# app/user.py
from app.config_helpers import ALLOWED_EXTENSIONS, allowed_file, MAX_FILE_SIZE, file_size_limit




def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash("You must be logged in as admin", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
def home_page():
    now = datetime.now()
    # Today range
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Ongoing = today
    ongoing_events = Event.query.filter(
        Event.time >= today_start,
        Event.time <= today_end
    ).order_by(Event.time.asc()).all()
    youtube_link = "https://www.youtube.com/watch?v=s8iBPV7Cm8M"
    
    # Extract video ID
    video_id = youtube_link.split("v=")[-1]

    # Optional: local cover image (you can use YouTube thumbnail too)
    cover_image = "/static/images/s2.jpg"

    sermon_data = {
        "title": "Faith That Moves Mountains",
        "video_id": video_id,
        "cover_image": cover_image
    }
    return render_template("index.html",ongoing_events=ongoing_events,sermon=sermon_data)



@app.route("/sermon")
def sermon():
    # Random YouTube video link
    youtube_link = "https://www.youtube.com/watch?v=s8iBPV7Cm8M"
    
    # Extract video ID
    video_id = youtube_link.split("v=")[-1]

    # Optional: local cover image (you can use YouTube thumbnail too)
    cover_image = "/static/images/s2.jpg"

    sermon_data = {
        "title": "Faith That Moves Mountains",
        "video_id": video_id,
        "cover_image": cover_image
    }

    return render_template("sermon.html", sermon=sermon_data)

@app.route("/about/us")
def about_us():
    return render_template("about.html")

@app.route("/contact/us")
def contact_us():
    return render_template("contact.html")


# ---------------------------
# Ordinal function (REQUIRED)
# ---------------------------
def ordinal(n):
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"


# ---------------------------
# Pretty date filter
# ---------------------------
@app.template_filter('pretty_date')
def pretty_date(value):
    if value is None:
        return ""
    return f"{ordinal(value.day)} {value.strftime('%B %Y, %I:%M %p')}"

# ---------------------------
# Custom Jinja filter: First image (skip videos)
# ---------------------------
@app.template_filter('first_image')
def first_image(event):
    """Return first image file, skip videos"""
    if event.files:
        for file in event.files:
            ext = os.path.splitext(file.filename)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                return url_for('static', filename='uploads/' + file.filename)

    return url_for('static', filename='images/default.jpg')

# ---------------------------
# Route to browse events
# ---------------------------
@app.get('/browse_event/')
def browse_event():
    now = datetime.now()

    # Today range
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Ongoing = today
    ongoing_events = Event.query.filter(
        Event.time >= today_start,
        Event.time <= today_end
    ).order_by(Event.time.asc()).all()

    # Upcoming = future
    upcoming_events = Event.query.filter(
        Event.time > today_end
    ).order_by(Event.time.asc()).all()

    # Concluded = past
    concluded_events = Event.query.filter(
        Event.time < today_start
    ).order_by(Event.time.desc()).all()

    print("ONGOING:", [e.title for e in ongoing_events])
    print("UPCOMING:", [e.title for e in upcoming_events])
    print("CONCLUDED:", [e.title for e in concluded_events])

    return render_template(
        "events.html",
        ongoing_events=ongoing_events,
        upcoming_events=upcoming_events,
        concluded_events=concluded_events
    )

@app.get('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_detail.html", event=event)


UPLOAD_FOLDER = 'static/media'

@app.route('/media/', methods=['GET', 'POST'])
def media_page():
    form = MediaForm()

    if form.validate_on_submit():
        files = form.file.data
        gallery_type = form.gallery_type.data
        title = form.title.data
        description = form.description.data

        # 🔥 FIX: Handle None safely
        if not files:
            flash("Please select a file.", "danger")
            return redirect(request.url)

        # 🔥 Restrict uploads
        if gallery_type != "Photo" and len(files) > 1:
            flash("You can only upload ONE file for this category.", "danger")
            return redirect(request.url)

        # unique batch id for grouping images
        batch_id = str(uuid.uuid4())

        for file in files:
            if file:  # extra safety
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

                media = Media(
                    gallery_type=gallery_type,
                    title=title,
                    filename=filename,
                    description=description,
                    batch_id=batch_id if gallery_type == "Photo" else None
                )
                db.session.add(media)

        db.session.commit()
        flash("Upload successful!", "success")
        return redirect(url_for('media_page'))

    # FETCH DATA
    photos = Media.query.filter_by(gallery_type="Photo").order_by(Media.created_at.desc()).all()
    videos = Media.query.filter_by(gallery_type="Video").order_by(Media.created_at.desc()).all()
    audios = Media.query.filter_by(gallery_type="Audio").order_by(Media.created_at.desc()).all()
    documents = Media.query.filter_by(gallery_type="Document").order_by(Media.created_at.desc()).all()

    return render_template(
        'media.html',
        form=form,
        photos=photos,
        videos=videos,
        audios=audios,
        documents=documents
    )   


# Set upload folder
UPLOAD_FOLDER = os.path.join('static', 'media')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # ensure folder exists

@app.route('/admin/add_media/', methods=['GET', 'POST'])
def add_media():
    form = MediaForm()

    if request.method == 'POST' and form.validate_on_submit():
        gallery_type = form.gallery_type.data
        title = form.title.data
        description = form.description.data
        files = form.file.data

        # Restrict uploads for non-photo types
        if gallery_type != "Photo" and len(files) > 1:
            flash("You can only upload ONE file for this category.", "danger")
            return redirect(request.url)

        # Unique batch id for grouping photos
        batch_id = str(uuid.uuid4()) if gallery_type == "Photo" else None

        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            media = Media(
                gallery_type=gallery_type,
                title=title,
                filename=filename,
                description=description,
                created_at=None  # let SQLAlchemy use default datetime
            )
            db.session.add(media)

        db.session.commit()
        flash(f"{len(files)} {gallery_type}(s) uploaded successfully!", "success")
        return redirect(url_for('add_media'))

    return render_template('add_media.html', form=form)



@app.route('/church/project', methods=['GET', 'POST'])
def project_page():
    return render_template('church-project.html')


@app.route("/donate")
def donate():
    return render_template("donation.html")


@app.route("/verify-payment/<reference>")
def verify_payment(reference):
    import requests

    headers = {
        "Authorization": "Bearer YOUR_SECRET_KEY"
    }

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url, headers=headers)
    data = response.json()

    if data["data"]["status"] == "success":
        return "Donation Successful ✅"
    else:
        return "Payment Failed ❌"


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():

    form = AdminLoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.password == form.password.data:

            session['admin_logged_in'] = True
            session['admin_id'] = admin.id

            flash("Login successful", "success")
            return redirect(url_for('admin_dashboard'))

        flash("Invalid email or password", "danger")
    return render_template("login.html", form=form)


@csrf.exempt
@app.route('/admin/contact/<int:id>/attend', methods=['POST'])
def mark_attended(id):

    contact = Contact.query.get_or_404(id)

    contact.contact_status = "attended"
    db.session.commit()

    return jsonify(success=True)


@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():

    if not session.get('admin_logged_in'):
        flash("Please login first", "danger")
        return redirect(url_for('admin_login'))
    contacts = Contact.query.order_by(Contact.date_sent.desc()).all()

    return render_template('admin-dashboard.html', contacts=contacts)



# @app.route('/admin/dashboard', methods=['GET','POST'])
# def admin_dashboard():
#     if not session.get('admin_logged_in'):
#         flash("Please login first", "danger")
#         return redirect(url_for('admin_login'))

#     form = GalleryForm()

#     # Handle gallery upload
#     if form.validate_on_submit():
#         file = form.file.data
#         filename = secure_filename(file.filename)
#         upload_folder = app.config['UPLOAD_FOLDER']
#         filepath = os.path.join(upload_folder, filename)

#         # Ensure folder exists
#         os.makedirs(upload_folder, exist_ok=True)

#         file.save(filepath)

#         # Save to database
#         new_item = Gallery(
#             gallery_type=form.gallery_type.data,
#             title=form.title.data,
#             ministry=form.ministry.data,
#             filename=filename,
#             description=form.description.data
#         )
#         db.session.add(new_item)
#         db.session.commit()

#         flash("Gallery item added successfully", "success")
#         return redirect(url_for('admin_dashboard'))

#     if form.errors:
#         print("FORM ERRORS:", form.errors)  # Debug any issues

#     contacts = Contact.query.order_by(Contact.date_sent.desc()).all()
#     return render_template('admin-dashboard.html', contacts=contacts, form=form)





from itsdangerous import URLSafeTimedSerializer as Serializer

# Initialize this with your app's secret key
s = Serializer(app.config['SECRET_KEY'])

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm() 
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin:
            # Generate Token
            token = s.dumps(admin.email, salt='password-reset-salt')
            # Use Flask-Mail to send email here (logic simplified)
            print(f"Reset Link: {url_for('reset_token', token=token, _external=True)}")
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('admin_login'))
        else:
            flash('There is no account with that email.', 'warning')
    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    try:
        # Link expires after 1800 seconds (30 mins)
        email = s.loads(token, salt='password-reset-salt', max_age=1800)
    except:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=email).first()
        # Update password in DB (Remember to hash it!)
        admin.password = form.password.data 
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('admin_login'))
    return render_template('reset_token.html', form=form)



# @app.route("/admin/add_event", methods=["GET", "POST"])
# def add_events():

#     form = EventForm()

#     if request.method == "POST":

#         files = request.files.getlist("files")

#         if not files:
#             flash("Please upload at least one file.", "danger")
#             return redirect(request.url)

#         for i, file in enumerate(files):

#             if file.filename == "":
#                 continue

#             if not allowed_file(file.filename):
#                 flash(f"{file.filename} is not allowed. Only images or videos are accepted.", "danger")
#                 return redirect(request.url)

#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

#             file.save(filepath)

#             title = request.form.get(f"title_{i}")
#             caption = request.form.get(f"caption_{i}")
#             ministry = request.form.get(f"ministry_{i}")
#             gallery_time = request.form.get(f"gallery_time_{i}")

#             new_event = Event(
#                 title=title,
#                 description=caption,
#                 ministry=ministry,
#                 created_at=gallery_time,
#                 filename=filename
#             )

#             db.session.add(new_event)

#         db.session.commit()

#         flash("Gallery items uploaded successfully!", "success")
#         return redirect(url_for("add_events"))

#     return render_template("add_events.html", form=form)



# @app.route("/admin/add_event", methods=["GET","POST"])
# @admin_required
# def add_event():
#     form = EventForm()
    
#     if form.validate_on_submit():
#         files = form.files.data

#         if not files:
#             flash("Please upload at least one file", "danger")
#             return render_template("add_event.html", form=form)

#         for file in files:
#             if file.filename == "":
#                 continue

#             if not allowed_file(file.filename):
#                 flash(f"{file.filename} has an invalid file type", "danger")
#                 return render_template("add_event.html", form=form)

#             if len(file.read()) > MAX_FILE_SIZE:
#                 file.seek(0)
#                 flash(f"{file.filename} exceeds max size of 20MB", "danger")
#                 return render_template("add_event.html", form=form)

#             file.seek(0)
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#             file.save(filepath)


#             uploaded_files = []
#             for file in files:
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#                 uploaded_files.append(filename)
            

#             event = Event(
#                 title=form.title.data,
#                 ministry=form.ministry.data,
#                 description=form.description.data,
#                 filename=",".join(uploaded_files)  # store all file names in one field
#             )

#             db.session.add(event)
#             db.session.commit()

#             event = Event(
#                 title=form.title.data,
#                 ministry=form.ministry.data,
#                 description=form.description.data
#                 )
#             db.session.add(event)
#             db.session.commit()  # commit first to get event.id

#             for file in files:
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#                 event_file = EventFile(event_id=event.id, filename=filename)
#                 db.session.add(event_file)

#             db.session.commit()


#         flash("Event uploaded successfully", "success")
#         return redirect(url_for("add_event"))
    
#     return render_template("add_event.html", form=form)

@app.get("/test")
def test():
    return render_template("test.html")

@app.route("/admin/add_event", methods=["GET","POST"])
@admin_required
def add_event():
    form = EventForm()
    
    if form.validate_on_submit():
        files = form.files.data or []

        if not files:
            flash("Please upload at least one file", "danger")
            return render_template("add_event.html", form=form)

        # Create Event first
        event = Event(
            title=form.title.data,
            ministry=form.ministry.data,
            venue=form.venue.data,
            time=form.time.data,
            description=form.description.data
        )
        db.session.add(event)
        db.session.commit()  # commit to get event.id

        # Save all files
        for file in files:
            if file.filename == "":
                continue
            if not allowed_file(file.filename):
                flash(f"{file.filename} has an invalid file type", "danger")
                db.session.delete(event)
                db.session.commit()
                return render_template("add_event.html", form=form)

            file.seek(0, 2)
            size = file.tell()
            file.seek(0)
            if size > MAX_FILE_SIZE:
                flash(f"{file.filename} exceeds max size of 20MB", "danger")
                db.session.delete(event)
                db.session.commit()
                return render_template("add_event.html", form=form)

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            event_file = EventFile(event_id=event.id, filename=filename)
            db.session.add(event_file)

        db.session.commit()
        flash("Event uploaded successfully with all files", "success")
        return redirect(url_for("add_event"))

    return render_template("add_event.html", form=form)



@app.route("/admin/update_event/<int:event_id>", methods=["GET", "POST"])
@admin_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = UpdateEventForm(obj=event)  # Pre-fill form with existing data

    if form.validate_on_submit():
        # Update text fields
        event.title = form.title.data
        event.ministry = form.ministry.data
        event.description = form.description.data
        event.venue = form.venue.data
        event.time = form.time.data

        files = form.files.data or []

        for file in files:
            if file.filename == "":
                continue

            if not allowed_file(file.filename):
                flash(f"{file.filename} has an invalid file type", "danger")
                return redirect(request.url)

            if len(file.read()) > MAX_FILE_SIZE:
                file.seek(0)
                flash(f"{file.filename} exceeds max size of 20MB", "danger")
                return redirect(request.url)

            file.seek(0)
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Replace the old file with the new one
            event.filename = filename

        db.session.commit()
        flash("Event updated successfully", "success")
        # return redirect(url_for("admin_dashboard"))
        return redirect(url_for("view_event", event_id=event.id)) #to redirect to event details page after update

    return render_template("update_event.html", form=form, event=event)


@app.route("/admin/view_event/<int:event_id>")
@admin_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("view_event.html", event=event)


@app.route("/admin/delete_event/<int:event_id>", methods=["POST","GET"])
@admin_required
def delete_event(event_id):
    # Fetch the event or return 404 if not found
    event = Event.query.get_or_404(event_id)

    # Delete the file from uploads folder (optional)
    if event.filename:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], event.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    # Delete the database record
    db.session.delete(event)
    db.session.commit()

    flash("Event deleted successfully!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

    

