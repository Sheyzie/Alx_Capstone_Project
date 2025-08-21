from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Student


User = get_user_model()

class StudentTest(APITestCase):
    def setUp(self):
        # create an student user
        self.client = APIClient()
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

        self.student = Student.objects.get(user__email='sample_student@mail.com')

        # login student

        url = reverse('token_obtain_pair')

        data = {
            'email': 'sample_student@mail.com',
            'password': 'student_Password',
        }

        response = self.client.post(url, data=data, content_type='application/json')

        # get token from response
        self.token = response.data.pop('access')

        # add token to header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_student_list(self):
        url = reverse('student_list')

        response = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'activated')
        self.assertEqual(bad_response.status_code, 401)

    def test_student_detail(self):
        url = reverse('student_detail', kwargs={'pk': self.student.pk})

        response = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'activated')
        self.assertEqual(bad_response.status_code, 401)

    def test_activate_student(self):
        # create super_user
        self.admin_user = User.objects.create_superuser(
            first_name='Sample',
            last_name='SuperAdmin',
            email='superadmin@mail.com',
            password='superadmin_Password'
        )

        # login super_user
        url = reverse('token_obtain_pair')

        data = {
            'email': 'superadmin@mail.com',
            'password': 'superadmin_Password',
        }

        response = self.client.post(url, data=data, content_type='application/json')

        # get token from response
        admin_token = response.data.pop('access')

        # add token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        # activate student
        url = reverse('student_activate', kwargs={'pk': self.student.pk})
        response = self.client.put(url, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'activated')
        self.assertEqual(bad_response.status_code, 401)

    def test_deactivate_student(self):
        # create super_user
        self.admin_user = User.objects.create_superuser(
            first_name='Sample',
            last_name='SuperAdmin',
            email='superadmin@mail.com',
            password='superadmin_Password'
        )

        # login super_user
        url = reverse('token_obtain_pair')

        data = {
            'email': 'superadmin@mail.com',
            'password': 'superadmin_Password',
        }

        response = self.client.post(url, data=data, content_type='application/json')

        # get token from response
        admin_token = response.data.pop('access')

        # add token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        # deactivate student
        url = reverse('student_deactivate', kwargs={'pk': self.student.pk})
        response = self.client.put(url, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'deactivated')
        self.assertEqual(bad_response.status_code, 401)

    def test_delete_student(self):
        # create super_user
        self.admin_user = User.objects.create_superuser(
            first_name='Sample',
            last_name='SuperAdmin',
            email='superadmin@mail.com',
            password='superadmin_Password'
        )

        # login super_user
        url = reverse('token_obtain_pair')

        data = {
            'email': 'superadmin@mail.com',
            'password': 'superadmin_Password',
        }

        response = self.client.post(url, data=data, content_type='application/json')

        # get token from response
        admin_token = response.data.pop('access')

        # add token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        # delete student
        url = reverse('student_delete', kwargs={'pk': self.student.pk})
        response = self.client.delete(url, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bad_response.status_code, 401)

