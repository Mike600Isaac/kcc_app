from flask import jsonify, render_template, request, flash, redirect, session, url_for
from wtforms import form
from app import app,csrf
from app.form import ContactForm,AdminLoginForm
from app.models import db,Contact,Admin


@app.route("/")
def home_page():
    return render_template("index.html")

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
    return render_template("admin_login.html", form=form)


@csrf.exempt
@app.route('/admin/contact/<int:id>/attend', methods=['POST'])
def mark_attended(id):

    contact = Contact.query.get_or_404(id)

    contact.contact_status = "attended"
    db.session.commit()

    return jsonify(success=True)


@app.route('/admin/dashboard')
def admin_dashboard():

    if not session.get('admin_logged_in'):
        flash("Please login first", "danger")
        return redirect(url_for('admin_login'))
    contacts = Contact.query.order_by(Contact.date_sent.desc()).all()

    return render_template('admin_dashboard.html', contacts=contacts)



@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

    

