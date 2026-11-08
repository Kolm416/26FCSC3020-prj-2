'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from .models import db, User, Competition
from datetime import datetime

main = Blueprint('main', __name__)

@main.get('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', '')
        if not name or len(name) > 120 or not email or len(email) > 255 or '@' not in email or not email.split('@')[-1].count('.'):
            flash('Enter a valid name and email address.', 'error')
        elif len(password) < 12:
            flash('Password must be at least 12 characters.', 'error')
        elif role not in ('participant', 'organizer'):
            flash('Select a valid role.', 'error')
        elif db.session.query(User.id).filter_by(email=email).first():
            flash('An account with that email already exists.', 'error')
        else:
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash('An account with that email already exists.', 'error')
            else:
                flash('Account created. Please log in.', 'success')
                return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = db.session.query(User).filter_by(email=email).first()
        if user and user.active and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')

@main.post('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'success')
    return redirect(url_for('main.index'))


# US2: Display competitions created by the organizer.
@main.get('/dashboard')
@login_required
def dashboard():

    # Only organizers can access this page.
    if current_user.role != 'organizer':
        flash('Only organizers can access this page.', 'error')
        return redirect(url_for('main.index'))

    # Retrieve competitions belonging to this organizer.
    competitions = db.session.query(Competition).filter_by(
        organizer_id=current_user.id
    ).order_by(Competition.start_date).all()

    # Display the organizer dashboard.
    return render_template(
        'dashboard.html',
        competitions=competitions
    )

# US3: Allow organizers to create new competitions.
@main.route('/competitions/create', methods=['GET', 'POST'])
@login_required
def create_competition():

    # Only organizers can create competitions.
    if current_user.role != 'organizer':
        flash('Only organizers can create competitions.', 'error')
        return redirect(url_for('main.index'))

    # Process the submitted form.
    if request.method == 'POST':

        # Retrieve form information.
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')

        # Check required fields.
        if not name or not description or not start_date or not end_date:
            flash('All fields are required.', 'error')
            return render_template('create_competition.html')

        # Validate competition name length.
        if len(name) > 120:
            flash('Competition name must be 120 characters or less.', 'error')
            return render_template('create_competition.html')

        # Convert dates from the HTML form.
        try:
            start = datetime.strptime(start_date, '%Y-%m-%dT%H:%M')
            end = datetime.strptime(end_date, '%Y-%m-%dT%H:%M')

        except ValueError:
            flash('Enter valid competition dates.', 'error')
            return render_template('create_competition.html')

        # Make sure the end date is after the start date.
        if end <= start:
            flash('End date must be after the start date.', 'error')
            return render_template('create_competition.html')

        # Create the competition.
        competition = Competition(
            name=name,
            description=description,
            start_date=start,
            end_date=end,
            organizer_id=current_user.id
        )

        # Save the competition to the database.
        db.session.add(competition)
        db.session.commit()

        # Return to the organizer dashboard.
        flash('Competition created successfully.', 'success')
        return redirect(url_for('main.dashboard'))

    # Display the creation form.
    return render_template('create_competition.html')
