'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from .models import db, User, Competition, Challenge, CompetitionRegistration
from datetime import datetime, timezone

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

# US4: Allow organizers to add challenges.
@main.route('/competitions/<int:competition_id>/challenges/create',
            methods=['GET', 'POST'])
@login_required
def create_challenge(competition_id):

    # Only organizers can create challenges.
    if current_user.role != 'organizer':
        flash('Only organizers can create challenges.', 'error')
        return redirect(url_for('main.index'))

    # Find the competition.
    competition = db.session.get(Competition, competition_id)

    # Check that the competition exists.
    if competition is None:
        flash('Competition not found.', 'error')
        return redirect(url_for('main.dashboard'))

    # Check that the organizer owns this competition.
    if competition.organizer_id != current_user.id:
        flash('You cannot modify this competition.', 'error')
        return redirect(url_for('main.dashboard'))

    # Process the submitted form.
    if request.method == 'POST':

        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        points_text = request.form.get('points', '').strip()
        flag = request.form.get('flag', '').strip()

        # Check required fields.
        if not title or not description or not category or not points_text or not flag:
            flash('All fields are required.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        # Validate text lengths.
        if len(title) > 120 or len(category) > 50 or len(flag) > 255:
            flash('One or more fields are too long.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        # Validate the point value.
        try:
            points = int(points_text)
        except ValueError:
            flash('Points must be a whole number.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        if points <= 0:
            flash('Points must be greater than zero.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        # Create the challenge.
        challenge = Challenge(
            title=title,
            description=description,
            category=category,
            points=points,
            flag=flag,
            competition_id=competition.id
        )

        # Save the challenge.
        db.session.add(challenge)
        db.session.commit()

        flash('Challenge created successfully.', 'success')

        return redirect(url_for('main.dashboard'))

    # Display the challenge form.
    return render_template(
        'create_challenge.html',
        competition=competition
    )

# US5: Display competitions available for registration.
@main.get('/competitions')
@login_required
def competitions():

    # Only participants can register for competitions.
    if current_user.role != 'participant':
        flash('Only participants can register for competitions.', 'error')
        return redirect(url_for('main.index'))

    # Get the current UTC date and time.
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Find competitions that have not started.
    available_competitions = db.session.query(Competition).filter(
        Competition.start_date > now
    ).order_by(Competition.start_date).all()

    # Find competitions this participant has already joined.
    registrations = db.session.query(CompetitionRegistration).filter_by(
        participant_id=current_user.id
    ).all()

    # Collect the IDs of registered competitions.
    registered_ids = []

    for registration in registrations:
        registered_ids.append(registration.competition_id)

    # Display the available competitions.
    return render_template(
        'competitions.html',
        competitions=available_competitions,
        registered_ids=registered_ids
    )

# US5: Register a participant for a competition.
@main.post('/competitions/<int:competition_id>/register')
@login_required
def register_competition(competition_id):

    # Only participants can register.
    if current_user.role != 'participant':
        flash('Only participants can register for competitions.', 'error')
        return redirect(url_for('main.index'))

    # Find the competition.
    competition = db.session.get(Competition, competition_id)

    if competition is None:
        flash('Competition not found.', 'error')
        return redirect(url_for('main.competitions'))

    # Get the current UTC date and time.
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Registration closes when the competition starts.
    if competition.start_date <= now:
        flash('Registration is closed for this competition.', 'error')
        return redirect(url_for('main.competitions'))

    # Check whether the participant is already registered.
    existing_registration = db.session.query(
        CompetitionRegistration
    ).filter_by(
        participant_id=current_user.id,
        competition_id=competition.id
    ).first()

    if existing_registration:
        flash('You are already registered for this competition.', 'error')
        return redirect(url_for('main.competitions'))

    # Create a new registration.
    registration = CompetitionRegistration(
        participant_id=current_user.id,
        competition_id=competition.id
    )

    # Save the registration.
    db.session.add(registration)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('You are already registered for this competition.', 'error')
        return redirect(url_for('main.competitions'))

    flash('Successfully registered for competition.', 'success')

    return redirect(url_for('main.competitions'))
