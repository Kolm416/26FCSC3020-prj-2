'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

"""US1 functional tests using Flask's black-box test client (not Selenium)."""
import pytest
from app import create_app
from app.models import db, User

@pytest.fixture
def app(tmp_path):
    return create_app({'TESTING': True, 'SECRET_KEY': 'test-key', 'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + str(tmp_path / 'test.sqlite3')})

def test_registration_and_login(app):
    client = app.test_client()
    response = client.post('/register', data={'name':'Alex', 'email':'Alex@Example.com', 'password':'correct-horse-123', 'role':'participant'}, follow_redirects=True)
    assert b'Account created' in response.data
    with app.app_context():
        user = db.session.query(User).filter_by(email='alex@example.com').one()
        assert user.role == 'participant'
        assert user.password_hash != 'correct-horse-123'
        assert user.check_password('correct-horse-123')
    response = client.post('/login', data={'email':'alex@example.com','password':'correct-horse-123'}, follow_redirects=True)
    assert b'Welcome, Alex!' in response.data
    response = client.post('/logout', follow_redirects=True)
    assert b'You have logged out.' in response.data

def test_duplicate_email(app):
    client = app.test_client()
    data={'name':'Alex','email':'alex@example.com','password':'correct-horse-123','role':'organizer'}
    client.post('/register', data=data)
    response=client.post('/register',data=data)
    assert b'already exists' in response.data
    with app.app_context():
        assert db.session.query(User).count() == 1

@pytest.mark.parametrize('change', [{'role':'admin'}, {'password':'short'}, {'name':''}, {'email':'invalid'}])
def test_invalid_registration(app, change):
    data={'name':'Alex','email':'alex@example.com','password':'correct-horse-123','role':'participant'}
    data.update(change)
    response=app.test_client().post('/register',data=data)
    assert response.status_code == 200
    with app.app_context():
        assert db.session.query(User).count() == 0

def test_invalid_login(app):
    response=app.test_client().post('/login',data={'email':'missing@example.com','password':'wrong'})
    assert b'Invalid email or password' in response.data
