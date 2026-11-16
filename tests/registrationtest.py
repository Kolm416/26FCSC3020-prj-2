'''
CSC3020 - Software Engineering Fundamentals
Instructor: Thyago Mota
Student(s): Juvia Archuleta, Leigha Lennon
Description: Project 2
'''

import unittest
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get("http://127.0.0.1:5000/register")

    def testRegistration(self):
        # Use a unique email so the account doesn't exist yet
        email = f"test_{uuid.uuid4().hex[:8]}@example.com"

        # Fill out the registration form
        self.browser.find_element(By.NAME, "name").send_keys("Test User")
        self.browser.find_element(By.NAME, "email").send_keys(email)
        self.browser.find_element(By.NAME, "password").send_keys("TestPassword123!")

        # Select the participant role
        role = Select(self.browser.find_element(By.NAME, "role"))
        role.select_by_value("participant")

        # Submit the form
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Wait for the login page
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("/login")
        )

        # Verify registration was successful
        message = self.browser.find_element(By.CSS_SELECTOR, "[role='status']").text
        self.assertIn("Account created. Please log in.", message)

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
