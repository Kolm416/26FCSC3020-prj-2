'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

"""Persistent user accounts for US1."""
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    creation_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Competition model for US2 and US3.
class Competition(db.Model):

    # Unique ID for each competition.
    id = db.Column(db.Integer, primary_key=True)

    # Competition information.
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Competition start and end dates.
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    # ID of the organizer who created the competition.
    organizer_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    # Relationship between competitions and organizers.
    organizer = db.relationship(
        'User',
        backref='competitions'
    )