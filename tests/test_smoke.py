'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

from app import create_app

def test_homepage():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"CTF Competition Platform" in response.data
