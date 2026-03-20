from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash


db=SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False) 
    message = db.Column(db.Text, nullable=False) 
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)


# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     ministry = db.Column(db.String(100), nullable=False)
#     filename = db.Column(db.String(300), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EventFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ministry = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    venue = db.Column(db.String(200), nullable=True)
    time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    files = db.relationship('EventFile', backref='event', lazy=True)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gallery_type = db.Column(db.String(50), nullable=False)  
    title = db.Column(db.String(200), nullable=False)
    ministry = db.Column(db.String(100), nullable=True)
    filename = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 👇 NEW (group multiple images under one title)
    batch_id = db.Column(db.String(100), nullable=True)
