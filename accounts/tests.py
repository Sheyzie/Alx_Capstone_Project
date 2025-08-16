from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import UserProfile


User = get_user_model()

class UserTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(
            first_name = 'sample',
            last_name = 'user',
            email='sample_user@mail.com',
            password='sample_user_Password'
        )

        user_profile = UserProfile.objects.create(
            user=user,
            role='student',
            bio='This is a sample user'
        )

        
        get_user = User.objects.get(first_name='sample')

        self.assertEqual(user.first_name, get_user.first_name)
        self.assertEqual(user.last_name, get_user.last_name)
        self.assertEqual(user.email, get_user.email)
        self.assertEqual(user_profile.role, get_user.profile.role)
        self.assertEqual(user_profile.bio, get_user.profile.bio)

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(
            first_name = 'sample',
            last_name = 'user',
            email='sample_user@mail.com',
            password='sample_user_Password'
        )

        profile = UserProfile.objects.create(
            user=user,
            role='student',
            bio='This is a sample user'
        )

        data = {
            'email':'sample_user@mail.com',
            'password':'sample_user_Password'           
        }

        response = self.client.post(url, data=data, content_type='application/json')


        self.assertEqual(response.status_code, 200)

