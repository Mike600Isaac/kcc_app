import os
from flask import jsonify, render_template, request, flash, redirect, session, url_for
from app import app,csrf
from app.form import GalleryForm,AdminLoginForm, ResetPasswordForm,RequestResetForm
from app.models import db,Contact,Admin,Gallery
from werkzeug.utils import secure_filename



@app.route("/")
def home_page():
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
    return render_template("index.html", sermon=sermon_data)



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

@app.get('/browse_event/')
def browse_event():
    return render_template('events.html')

@app.route('/gallery/', methods=['GET', 'POST'])
def gallery_page():
    return render_template('gallery.html')

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


# @app.route('/admin/dashboard')
# def admin_dashboard():

#     if not session.get('admin_logged_in'):
#         flash("Please login first", "danger")
#         return redirect(url_for('admin_login'))
#     contacts = Contact.query.order_by(Contact.date_sent.desc()).all()

#     return render_template('admin-dashboard.html', contacts=contacts)



@app.route('/admin/dashboard', methods=['GET','POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Please login first", "danger")
        return redirect(url_for('admin_login'))

    form = GalleryForm()

    # Handle gallery upload
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        filepath = os.path.join(upload_folder, filename)

        # Ensure folder exists
        os.makedirs(upload_folder, exist_ok=True)

        file.save(filepath)

        # Save to database
        new_item = Gallery(
            gallery_type=form.gallery_type.data,
            title=form.title.data,
            ministry=form.ministry.data,
            filename=filename,
            description=form.description.data
        )
        db.session.add(new_item)
        db.session.commit()

        flash("Gallery item added successfully", "success")
        return redirect(url_for('admin_dashboard'))

    if form.errors:
        print("FORM ERRORS:", form.errors)  # Debug any issues

    contacts = Contact.query.order_by(Contact.date_sent.desc()).all()
    return render_template('admin-dashboard.html', contacts=contacts, form=form)





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


# import os
# from werkzeug.utils import secure_filename

# @app.route("/admin/gallery", methods=["GET","POST"])
# def add_gallery():

#     form = GalleryForm()

#     if form.validate_on_submit():
#         print("FORM VALIDATED")

#         file = form.file.data
#         filename = secure_filename(file.filename)   

#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         new_item = Gallery(
#             gallery_type=form.gallery_type.data,
#             title=form.title.data,
#             ministry=form.ministry.data,
#             filename=filename,
#             description=form.description.data
#         )

#         db.session.add(new_item)
#         db.session.commit()

#         print("REQUEST METHOD:", request.method)

#         flash("Gallery item added successfully", "success")
#         return redirect(url_for("add_gallery"))

#     if form.errors:
#         print("FORM ERRORS:", form.errors)

#     return render_template("admin_gallery.html", form=form)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

    

