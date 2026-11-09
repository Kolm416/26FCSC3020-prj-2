'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''


from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize the SQLAlchemy database.
db = SQLAlchemy()


# US1: User registration and authentication.
class User(UserMixin, db.Model):

    # Unique identifier for each user.
    id = db.Column(db.Integer, primary_key=True)

    # User's full name.
    name = db.Column(db.String(120), nullable=False)

    # Unique email address used for login.
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    # Store the hashed password instead of plaintext.
    password_hash = db.Column(db.String(255), nullable=False)

    # User role: organizer or participant.
    role = db.Column(db.String(20), nullable=False)

    # Indicates whether the account is active.
    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    # Date and time the account was created.
    creation_date = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )

    # Hash the password before storing it.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify a password against the stored hash.
    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


# US2 and US3: Competition management.
class Competition(db.Model):

    # Unique identifier for each competition.
    id = db.Column(db.Integer, primary_key=True)

    # Competition name.
    name = db.Column(db.String(120), nullable=False)

    # Competition description.
    description = db.Column(db.Text, nullable=False)

    # Competition start date and time in UTC.
    start_date = db.Column(db.DateTime, nullable=False)

    # Competition end date and time in UTC.
    end_date = db.Column(db.DateTime, nullable=False)

    # Organizer who created the competition.
    organizer_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    # Relationship between organizers and competitions.
    organizer = db.relationship(
        'User',
        backref='competitions'
    )


# US4 and US6: Competition challenges and flag verification.
class Challenge(db.Model):

    # Unique identifier for each challenge.
    id = db.Column(db.Integer, primary_key=True)

    # Challenge title.
    title = db.Column(db.String(120), nullable=False)

    # Challenge instructions or description.
    description = db.Column(db.Text, nullable=False)

    # Challenge category.
    category = db.Column(db.String(50), nullable=False)

    # Points awarded for solving the challenge.
    points = db.Column(db.Integer, nullable=False)

    # Store the hashed flag instead of the original flag.
    flag_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # Competition that contains the challenge.
    competition_id = db.Column(
        db.Integer,
        db.ForeignKey('competition.id'),
        nullable=False
    )

    # Relationship between competitions and challenges.
    competition = db.relationship(
        'Competition',
        backref='challenges'
    )

    # Hash the correct flag before saving it.
    def set_flag(self, flag):
        self.flag_hash = generate_password_hash(flag)

    # Verify a submitted flag against the stored hash.
    def check_flag(self, submitted_flag):
        return check_password_hash(
            self.flag_hash,
            submitted_flag
        )


# US5: Participant competition registration.
class CompetitionRegistration(db.Model):

    # Unique identifier for each registration.
    id = db.Column(db.Integer, primary_key=True)

    # Participant registering for the competition.
    participant_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    # Competition the participant registered for.
    competition_id = db.Column(
        db.Integer,
        db.ForeignKey('competition.id'),
        nullable=False
    )

    # Prevent a participant from registering twice
    # for the same competition.
    __table_args__ = (
        db.UniqueConstraint(
            'participant_id',
            'competition_id',
            name='unique_competition_registration'
        ),
    )



# US6: Record each challenge solved by a participant.
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('participant_id', 'challenge_id', name='unique_challenge_solution'),
    )
