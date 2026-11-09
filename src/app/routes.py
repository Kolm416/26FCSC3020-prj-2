'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

from datetime import datetime, timezone
from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from flask_login import (current_user, login_user, logout_user, login_required)
from sqlalchemy.exc import IntegrityError
from .models import (db, User, Competition, Challenge, CompetitionRegistration, Submission)


# Create the main application blueprint.
main = Blueprint('main', __name__)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@main.get('/')
def index():

    return render_template('index.html')


# --------------------------------------------------
# US1: User Registration
# --------------------------------------------------

@main.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', '').strip()

        # Validate required fields.
        if not name or not email or not password or not role:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        # Validate input lengths.
        if len(name) > 120 or len(email) > 255:
            flash('Name or email is too long.', 'error')
            return render_template('register.html')

        # Validate basic email format.
        if (
            '@' not in email
            or '.' not in email.split('@')[-1]
        ):
            flash('Invalid email address.', 'error')
            return render_template('register.html')

        # Require a password of at least 12 characters.
        if len(password) < 12:
            flash('Password must be at least 12 characters.', 'error')
            return render_template('register.html')

        # Only allow supported account roles.
        if role not in ('organizer', 'participant'):
            flash('Invalid role selected.', 'error')
            return render_template('register.html')

        # Check whether the email is already registered.
        existing_user = db.session.query(User).filter_by(
            email=email
        ).first()

        if existing_user:
            flash('Email already exists.', 'error')
            return render_template('register.html')

        # Create the user.
        user = User(
            name=name,
            email=email,
            role=role
        )

        # Hash the password before saving.
        user.set_password(password)

        db.session.add(user)

        try:
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            flash('Email already exists.', 'error')
            return render_template('register.html')

        flash('Account created. Please log in.', 'success')

        return redirect(url_for('main.login'))

    return render_template('register.html')


# --------------------------------------------------
# US1: User Login
# --------------------------------------------------

@main.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Find the user by email.
        user = db.session.query(User).filter_by(
            email=email
        ).first()

        # Verify the password and account status.
        if (
            user is None
            or not user.active
            or not user.check_password(password)
        ):
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        # Log in the user.
        login_user(user)

        flash('Login successful.', 'success')

        return redirect(url_for('main.index'))

    return render_template('login.html')


# --------------------------------------------------
# US1: User Logout
# --------------------------------------------------

@main.post('/logout')
@login_required
def logout():

    logout_user()

    flash('You have logged out.', 'success')

    return redirect(url_for('main.index'))


# --------------------------------------------------
# US2: Organizer Dashboard
# --------------------------------------------------

@main.get('/dashboard')
@login_required
def dashboard():

    # Only organizers may access this page.
    if current_user.role != 'organizer':
        flash('Only organizers can access this page.', 'error')
        return redirect(url_for('main.index'))

    # Retrieve competitions belonging to this organizer.
    competitions = db.session.query(Competition).filter_by(
        organizer_id=current_user.id
    ).order_by(
        Competition.start_date
    ).all()

    return render_template(
        'dashboard.html',
        competitions=competitions
    )


# --------------------------------------------------
# US3: Create Competition
# --------------------------------------------------

@main.route('/competitions/create', methods=['GET', 'POST'])
@login_required
def create_competition():

    # Only organizers may create competitions.
    if current_user.role != 'organizer':
        flash('Only organizers can create competitions.', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        start_date_text = request.form.get('start_date', '').strip()
        end_date_text = request.form.get('end_date', '').strip()

        # Validate required fields.
        if not all((
            name,
            description,
            start_date_text,
            end_date_text
        )):
            flash('All fields are required.', 'error')
            return render_template('create_competition.html')

        # Validate competition name length.
        if len(name) > 120:
            flash('Competition name is too long.', 'error')
            return render_template('create_competition.html')

        # Convert submitted UTC date strings into datetime objects.
        try:
            start_date = datetime.strptime(
                start_date_text,
                '%Y-%m-%dT%H:%M'
            )

            end_date = datetime.strptime(
                end_date_text,
                '%Y-%m-%dT%H:%M'
            )

        except ValueError:
            flash('Invalid date format.', 'error')
            return render_template('create_competition.html')

        # The end date must be later than the start date.
        if end_date <= start_date:
            flash(
                'End date must be after the start date.',
                'error'
            )
            return render_template('create_competition.html')

        # Dates are stored as naive UTC values.
        # The organizer enters UTC in the form.
        competition = Competition(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            organizer_id=current_user.id
        )

        db.session.add(competition)
        db.session.commit()

        flash('Competition created successfully.', 'success')

        return redirect(url_for('main.dashboard'))

    return render_template('create_competition.html')


# --------------------------------------------------
# US4: Create Challenge
# --------------------------------------------------

@main.route(
    '/competitions/<int:competition_id>/challenges/create',
    methods=['GET', 'POST']
)
@login_required
def create_challenge(competition_id):

    # Only organizers may create challenges.
    if current_user.role != 'organizer':
        flash('Only organizers can create challenges.', 'error')
        return redirect(url_for('main.index'))

    # Retrieve the competition.
    competition = db.session.get(
        Competition,
        competition_id
    )

    if competition is None:
        flash('Competition not found.', 'error')
        return redirect(url_for('main.dashboard'))

    # Prevent organizers from editing other organizers'
    # competitions.
    if competition.organizer_id != current_user.id:
        flash(
            'You cannot modify this competition.',
            'error'
        )
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':

        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        points_text = request.form.get('points', '').strip()

        # Do not strip the flag.
        # Flag verification will use the exact submitted value.
        flag = request.form.get('flag', '')

        # Validate required fields.
        if not all((
            title,
            description,
            category,
            points_text,
            flag
        )):
            flash('All fields are required.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        # Validate input lengths.
        if len(title) > 120:
            flash('Challenge title is too long.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        if len(category) > 50:
            flash('Challenge category is too long.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        if len(flag) > 255:
            flash('Flag is too long.', 'error')
            return render_template(
                'create_challenge.html',
                competition=competition
            )

        # Points must be greater than zero.
        try:
            points = int(points_text)

        except ValueError:
            flash('Points must be greater than zero.', 'error')
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

        # Create the challenge without storing plaintext flags.
        challenge = Challenge(
            title=title,
            description=description,
            category=category,
            points=points,
            competition_id=competition.id
        )

        # Hash the correct flag before saving the challenge.
        challenge.set_flag(flag)

        db.session.add(challenge)
        db.session.commit()

        flash('Challenge created successfully.', 'success')

        return redirect(url_for('main.dashboard'))

    return render_template(
        'create_challenge.html',
        competition=competition
    )


# --------------------------------------------------
# US5: View Upcoming Competitions
# --------------------------------------------------

@main.get('/competitions')
@login_required
def competitions():

    # Only participants may use the registration page.
    if current_user.role != 'participant':
        flash(
            'Only participants can register for competitions.',
            'error'
        )
        return redirect(url_for('main.index'))

    # Current UTC time, stored without timezone information.
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Retrieve competitions that have not started.
    available_competitions = db.session.query(
        Competition
    ).filter(
        Competition.start_date > now
    ).order_by(
        Competition.start_date
    ).all()

    # Retrieve this participant's existing registrations.
    registrations = db.session.query(
        CompetitionRegistration
    ).filter_by(
        participant_id=current_user.id
    ).all()

    registered_ids = []

    for registration in registrations:
        registered_ids.append(registration.competition_id)

    # Registered competitions currently in progress (US6).
    active_competitions = db.session.query(Competition).join(
        CompetitionRegistration,
        CompetitionRegistration.competition_id == Competition.id
    ).filter(
        CompetitionRegistration.participant_id == current_user.id,
        Competition.start_date <= now,
        Competition.end_date > now
    ).order_by(Competition.end_date).all()

    return render_template(
        'competitions.html',
        competitions=available_competitions,
        registered_ids=registered_ids,
        active_competitions=active_competitions
    )


# --------------------------------------------------
# US5: Register for Competition
# --------------------------------------------------

@main.post('/competitions/<int:competition_id>/register')
@login_required
def register_competition(competition_id):

    # Only participants may register.
    if current_user.role != 'participant':
        flash(
            'Only participants can register for competitions.',
            'error'
        )
        return redirect(url_for('main.index'))

    # Find the requested competition.
    competition = db.session.get(
        Competition,
        competition_id
    )

    if competition is None:
        flash('Competition not found.', 'error')
        return redirect(url_for('main.competitions'))

    # Check whether registration is still open.
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    if competition.start_date <= now:
        flash(
            'Registration is closed for this competition.',
            'error'
        )
        return redirect(url_for('main.competitions'))

    # Prevent duplicate registrations.
    existing_registration = db.session.query(
        CompetitionRegistration
    ).filter_by(
        participant_id=current_user.id,
        competition_id=competition.id
    ).first()

    if existing_registration:
        flash(
            'You are already registered for this competition.',
            'error'
        )
        return redirect(url_for('main.competitions'))

    # Create the participant registration.
    registration = CompetitionRegistration(
        participant_id=current_user.id,
        competition_id=competition.id
    )

    db.session.add(registration)

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        flash(
            'You are already registered for this competition.',
            'error'
        )

        return redirect(url_for('main.competitions'))

    flash(
        'Successfully registered for competition.',
        'success'
    )

    return redirect(url_for('main.competitions'))


# --------------------------------------------------
# US6: View Challenges and Submit Flags
# --------------------------------------------------

@main.route('/competitions/<int:competition_id>/challenges', methods=['GET', 'POST'])
@login_required
def competition_challenges(competition_id):

    if current_user.role != 'participant':
        flash('Only participants can submit flags.', 'error')
        return redirect(url_for('main.index'))

    competition = db.session.get(Competition, competition_id)
    if competition is None:
        flash('Competition not found.', 'error')
        return redirect(url_for('main.competitions'))

    registration = db.session.query(CompetitionRegistration).filter_by(
        participant_id=current_user.id,
        competition_id=competition_id
    ).first()
    if registration is None:
        flash('You must register for this competition first.', 'error')
        return redirect(url_for('main.competitions'))

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if not (competition.start_date <= now < competition.end_date):
        flash('This competition is not active.', 'error')
        return redirect(url_for('main.competitions'))

    if request.method == 'POST':
        challenge_id = request.form.get('challenge_id', type=int)
        submitted_flag = request.form.get('flag', '')
        challenge = db.session.get(Challenge, challenge_id) if challenge_id else None

        # The challenge must belong to this competition.
        if challenge is None or challenge.competition_id != competition.id:
            flash('Challenge not found.', 'error')
        elif not submitted_flag:
            flash('Enter a flag.', 'error')
        else:
            solved = db.session.query(Submission).filter_by(
                participant_id=current_user.id,
                challenge_id=challenge.id
            ).first()
            if solved:
                flash('You have already solved this challenge.', 'error')
            elif challenge.check_flag(submitted_flag):
                db.session.add(Submission(
                    participant_id=current_user.id,
                    challenge_id=challenge.id
                ))
                try:
                    db.session.commit()
                    flash('Correct flag! Points awarded.', 'success')
                except IntegrityError:
                    db.session.rollback()
                    flash('You have already solved this challenge.', 'error')
            else:
                flash('Incorrect flag. Try again.', 'error')

        return redirect(url_for('main.competition_challenges', competition_id=competition.id))

    challenges = db.session.query(Challenge).filter_by(
        competition_id=competition.id
    ).order_by(Challenge.id).all()

    submissions = db.session.query(Submission).join(
        Challenge, Submission.challenge_id == Challenge.id
    ).filter(
        Submission.participant_id == current_user.id,
        Challenge.competition_id == competition.id
    ).all()
    solved_ids = [submission.challenge_id for submission in submissions]
    points = sum(challenge.points for challenge in challenges if challenge.id in solved_ids)

    return render_template(
        'competition_challenges.html',
        competition=competition,
        challenges=challenges,
        solved_ids=solved_ids,
        points=points
    )


# --------------------------------------------------
# US7: Competition Rankings
# --------------------------------------------------

@main.get('/competitions/<int:competition_id>/rankings')
@login_required
def competition_rankings(competition_id):
    competition = db.session.get(Competition, competition_id)
    if competition is None:
        flash('Competition not found.', 'error')
        return redirect(url_for('main.index'))

    # Organizers can see rankings for their own competitions.
    # Participants must be registered for the competition.
    if current_user.role == 'organizer':
        if competition.organizer_id != current_user.id:
            flash('You cannot view this competition.', 'error')
            return redirect(url_for('main.dashboard'))
    elif current_user.role == 'participant':
        registration = db.session.query(CompetitionRegistration).filter_by(
            participant_id=current_user.id,
            competition_id=competition_id
        ).first()
        if registration is None:
            flash('You must register for this competition first.', 'error')
            return redirect(url_for('main.competitions'))
    else:
        return redirect(url_for('main.index'))

    # Include every registered participant, even those with zero points.
    registrations = db.session.query(CompetitionRegistration).filter_by(
        competition_id=competition_id
    ).all()
    challenges = db.session.query(Challenge).filter_by(
        competition_id=competition_id
    ).all()
    challenge_points = {challenge.id: challenge.points for challenge in challenges}

    # Read successful solutions and add each challenge's points.
    scores = {}
    for registration in registrations:
        scores[registration.participant_id] = 0

    submissions = db.session.query(Submission).join(
        Challenge, Submission.challenge_id == Challenge.id
    ).filter(Challenge.competition_id == competition_id).all()
    for submission in submissions:
        if submission.participant_id in scores:
            scores[submission.participant_id] += challenge_points[submission.challenge_id]

    rankings = []
    for registration in registrations:
        participant = db.session.get(User, registration.participant_id)
        rankings.append({
            'name': participant.name,
            'points': scores[registration.participant_id]
        })

    rankings.sort(key=lambda entry: (-entry['points'], entry['name'].lower()))

    # Equal scores receive the same rank.
    previous_points = None
    current_rank = 0
    for position, entry in enumerate(rankings, start=1):
        if entry['points'] != previous_points:
            current_rank = position
        entry['rank'] = current_rank
        previous_points = entry['points']

    return render_template(
        'competition_rankings.html',
        competition=competition,
        rankings=rankings
    )
