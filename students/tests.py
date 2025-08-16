from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentTest(TestCase):
    
    def test_create_instructor(self):
        url = reverse('student_register')
        data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'student',
                'email': 'sample_student@mail.com',
                'password': 'student_Password',
                'profile': {
                    "bio": "This is a test",
                    "avatar": None
                }
            },
        }

        response = self.client.post(url, data=data, content_type='application/json')

        self.assertEqual(response.status_code, 201)

    def test_student_login(self):
        signup_url = reverse('student_register')
        login_url = reverse('token_obtain_pair')
        signup_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'student',
                'email': 'sample_student@mail.com',
                'password': 'student_Password',
                'profile': {
                    "bio": "This is a test",
                    "avatar": None
                }
            },
        }

        login_data = {
            'email': 'sample_student@mail.com',
            'password': 'student_Password',
        }

        signup_response = self.client.post(signup_url, data=signup_data, content_type='application/json')
        login_response = self.client.post(login_url, data=login_data, content_type='application/json')

        self.assertEqual(signup_response.status_code, 201)
        self.assertEqual(login_response.status_code, 200)



