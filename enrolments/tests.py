from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from instructors.models import Instructor
from students.models import Student

from .models import Course, Lesson, LessonVideo, Enrolment


User = get_user_model()

class CourseTest(APITestCase):
    def setUp(self):
        self.superadmin = User.objects.create_superuser(
            first_name='Sample',
            last_name='Superuser',
            email='superuser@mail.com',
            password='superuser_Password'
        )

        data = {
            'email':'superuser@mail.com',
            'password':'superuser_Password'
        }

        response = self.client.post('/api/token/', data=data, content_type='application/json')

        # extract token from response
        self.token = response.data.pop('access')

        instructor_url = reverse('instructor_register')
        student_url = reverse('student_register')

        instructor_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'instructor',
                'email': 'sample_instructor@mail.com',
                'password': 'instructor_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        student_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'student',
                'email': 'sample_student@mail.com',
                'password': 'student_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        response = self.client.post(instructor_url, data=instructor_data, content_type='application/json')
        response = self.client.post(student_url, data=student_data, content_type='application/json')

        self.instructor = Instructor.objects.get(user__email='sample_instructor@mail.com')
        self.student = Student.objects.get(user__email='sample_student@mail.com')

    def test_course_creation(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response = self.client.post(url, data=data, content_type='application/json')
        self.client = APIClient()
        bad_response = self.client.get(url)
        # print(response.data)
        # print(self.client._credentials)
        # self.assertTrue(login_success)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(bad_response.status_code, 401)

    def test_course_list(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        url = reverse('course_list')
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Sample Course')
        self.assertContains(response2, 'Description of a sample course')
        self.assertEqual(bad_response.status_code, 401)

    def test_course_detail(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        course = Course.objects.get(title='Sample Course')

        url = reverse('course_detail', args=(course.id,))
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Sample Course')
        self.assertContains(response2, 'Description of a sample course')
        self.assertEqual(bad_response.status_code, 401)

    def test_course_update(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        course = Course.objects.get(title='Sample Course')

        data = {
            'title': 'Updated Sample Course',
            'description': 'Updated Description of a sample course',
            'status': 'inactive'
        }

        url = reverse('course_update', kwargs={'pk': course.pk})
        response2 = self.client.put(url, data=data, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.put(url, data=data, content_type='application/json')

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Updated Sample Course')
        self.assertContains(response2, 'Updated Description of a sample course')
        self.assertEqual(bad_response.status_code, 401)

    def test_course_delete(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        course = Course.objects.get(title='Sample Course')

        url = reverse('course_delete', kwargs={'pk': course.pk})
        response2 = self.client.delete(url)

        self.client = APIClient()
        bad_response = self.client.delete(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 204)
        self.assertEqual(bad_response.status_code, 401)

class LessonTest(APITestCase):
    def setUp(self):
        self.superadmin = User.objects.create_superuser(
            first_name='Sample',
            last_name='Superuser',
            email='superuser@mail.com',
            password='superuser_Password'
        )

        data = {
            'email':'superuser@mail.com',
            'password':'superuser_Password'
        }

        response = self.client.post('/api/token/', data=data, content_type='application/json')

        # extract token from response
        self.token = response.data.pop('access')

        instructor_url = reverse('instructor_register')
        student_url = reverse('student_register')

        instructor_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'instructor',
                'email': 'sample_instructor@mail.com',
                'password': 'instructor_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        student_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'student',
                'email': 'sample_student@mail.com',
                'password': 'student_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        response = self.client.post(instructor_url, data=instructor_data, content_type='application/json')
        response = self.client.post(student_url, data=student_data, content_type='application/json')

        self.instructor = Instructor.objects.get(user__email='sample_instructor@mail.com')
        self.student = Student.objects.get(user__email='sample_student@mail.com')

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        course_url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response = self.client.post(course_url, data=data, content_type='application/json')
        self.course = Course.objects.get(title='Sample Course')

    def test_lesson_creation(self):
        
        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response = self.client.post(url, data=data, content_type='application/json')
        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_list(self):
        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        url = reverse('lesson_list')
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Sample Lesson')
        self.assertContains(response2, '<h1>Sample Lesson</h1><p>A sample content</p>')
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_detail(self):
        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        lesson = Lesson.objects.get(title='Sample Lesson')

        url = reverse('lesson_detail', args=(lesson.id,))
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Sample Lesson')
        self.assertContains(response2, '<h1>Sample Lesson</h1><p>A sample content</p>')
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_update(self):
        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        lesson = Lesson.objects.get(title='Sample Lesson')

        data = {
            'title': 'Updated Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>An updated sample content</p>',
            'order': 2
        }

        url = reverse('lesson_update', kwargs={'pk': lesson.pk})
        response2 = self.client.put(url, data=data, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.put(url, data=data, content_type='application/json')

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Updated Sample Lesson')
        self.assertContains(response2, '<h1>Sample Lesson</h1><p>An updated sample content</p>')
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_delete(self):
        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        lesson = Lesson.objects.get(title='Sample Lesson')

        url = reverse('lesson_delete', kwargs={'pk': lesson.pk})
        response2 = self.client.delete(url)
 
        self.client = APIClient()
        bad_response = self.client.delete(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 204)
        self.assertEqual(bad_response.status_code, 401)

class LessonVideoTest(APITestCase):
    def setUp(self):
        self.superadmin = User.objects.create_superuser(
            first_name='Sample',
            last_name='Superuser',
            email='superuser@mail.com',
            password='superuser_Password'
        )

        data = {
            'email':'superuser@mail.com',
            'password':'superuser_Password'
        }

        response = self.client.post('/api/token/', data=data, content_type='application/json')

        # extract token from response
        self.token = response.data.pop('access')

        instructor_url = reverse('instructor_register')
        student_url = reverse('student_register')

        instructor_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'instructor',
                'email': 'sample_instructor@mail.com',
                'password': 'instructor_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        student_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'student',
                'email': 'sample_student@mail.com',
                'password': 'student_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        response = self.client.post(instructor_url, data=instructor_data, content_type='application/json')
        response = self.client.post(student_url, data=student_data, content_type='application/json')

        self.instructor = Instructor.objects.get(user__email='sample_instructor@mail.com')
        self.student = Student.objects.get(user__email='sample_student@mail.com')

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        course_url = reverse('course_create')
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'inactive'
        }

        response = self.client.post(course_url, data=data, content_type='application/json')
        self.course = Course.objects.get(title='Sample Course')

        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response = self.client.post(url, data=data, content_type='application/json')

        self.lesson = Lesson.objects.get(title='Sample Lesson')

    def test_lesson_video_creation(self):
        
        url = reverse('lesson_video_create')
        data = {
            'lesson': self.lesson.id,
            'url': 'https://sampleurl.com',
            'title': 'Sample Lesson',
            'order': 1
        }

        response = self.client.post(url, data=data, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_video_list(self):
        url = reverse('lesson_video_create')
        data = {
            'lesson': self.lesson.id,
            'url': 'https://sampleurl.com',
            'title': 'Sample Lesson',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        url = reverse('lesson_video_list')
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Sample Lesson')
        self.assertContains(response2, 'https://sampleurl.com')
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_video_detail(self):
        url = reverse('lesson_video_create')
        data = {
            'lesson': self.lesson.id,
            'url': 'https://sampleurl.com',
            'title': 'Sample Lesson',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        lesson_video = LessonVideo.objects.get(title='Sample Lesson')

        url = reverse('lesson_video_detail', args=(lesson_video.id,))
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Sample Lesson')
        self.assertContains(response2, 'https://sampleurl.com')
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_video_update(self):
        url = reverse('lesson_video_create')
        data = {
            'lesson': self.lesson.id,
            'url': 'https://sampleurl.com',
            'title': 'Sample Lesson',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        lesson_video = LessonVideo.objects.get(title='Sample Lesson')

        data = {
            'url': 'https://sampleurlupdated.com',
            'title': 'Updated Sample Lesson',
            'order': 1
        }

        url = reverse('lesson_video_update', kwargs={'pk': lesson_video.pk})
        response2 = self.client.put(url, data=data, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.put(url, data=data, content_type='application/json')

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Updated Sample Lesson')
        self.assertContains(response2, 'https://sampleurlupdated.com')
        self.assertEqual(bad_response.status_code, 401)

    def test_lesson_delete(self):
        url = reverse('lesson_video_create')
        data = {
            'lesson': self.lesson.id,
            'url': 'https://sampleurl.com',
            'title': 'Sample Lesson',
            'order': 1
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        lesson_video = LessonVideo.objects.get(title='Sample Lesson')

        url = reverse('lesson_video_delete', kwargs={'pk': lesson_video.pk})
        response2 = self.client.delete(url)
 
        self.client = APIClient()
        bad_response = self.client.delete(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 204)
        self.assertEqual(bad_response.status_code, 401)

class EnrolmentTest(APITestCase):
    def setUp(self):
        # creating a super admin user
        self.superadmin = User.objects.create_superuser(
            first_name='Sample',
            last_name='Superuser',
            email='superuser@mail.com',
            password='superuser_Password'
        )

        data = {
            'email':'superuser@mail.com',
            'password':'superuser_Password'
        }

        # login in as super admin
        response = self.client.post('/api/token/', data=data, content_type='application/json')

        # extract token from response
        self.admin_token = response.data.pop('access')
        
        # creating instructor and student
        instructor_url = reverse('instructor_register')
        student_url = reverse('student_register')

        instructor_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'instructor',
                'email': 'sample_instructor@mail.com',
                'password': 'instructor_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        student_data = {
            'user': {
                'first_name': 'sample',
                'last_name': 'student',
                'email': 'sample_student@mail.com',
                'password': 'student_Password',
                'profile': {
                    'bio': 'This is a test',
                    'avatar': None
                }
            },
        }

        response = self.client.post(instructor_url, data=instructor_data, content_type='application/json')
        response = self.client.post(student_url, data=student_data, content_type='application/json')

        self.instructor = Instructor.objects.get(user__email='sample_instructor@mail.com')
        self.student = Student.objects.get(user__email='sample_student@mail.com')

        # set admin token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # creating course
        course_url = reverse('course_create')
        
        data = {
            'title': 'Sample Course',
            'description': 'Description of a sample course',
            'instructor': self.instructor.id,
            'status': 'active'
        }

        response = self.client.post(course_url, data=data, content_type='application/json')
        self.course = Course.objects.get(title='Sample Course')

        url = reverse('lesson_create')
        data = {
            'course': self.course.id,
            'title': 'Sample Lesson',
            'content': '<h1>Sample Lesson</h1><p>A sample content</p>',
            'order': 1
        }

        response = self.client.post(url, data=data, content_type='application/json')

        # creating lesson
        self.lesson = Lesson.objects.get(title='Sample Lesson')

        url = reverse('lesson_video_create')

        data = {
            'lesson': self.lesson.id,
            'url': 'https://sampleurl.com',
            'title': 'Sample Lesson',
            'order': 1
        }

        self.lesson_video = self.client.post(url, data=data, content_type='application/json')

        # login as student
        data = {
            'email': 'sample_student@mail.com',
            'password': 'student_Password',
        }

        response = self.client.post('/api/token/', data=data, content_type='application/json')

        # extract token from response
        self.student_token = response.data.pop('access')

    def test_enrolment_creation(self):
        # add student token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        
        url = reverse('enrolement_create')

        data = {
            'course': self.course.id,
        }

        response = self.client.post(url, data=data, content_type='application/json')
        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(bad_response.status_code, 401)

    def test_enrolment_list(self):
        # add student token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        
        url = reverse('enrolement_create')

        data = {
            'course': self.course.id,
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        url = reverse('enrolement_list')
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'sample_student@mail.com')
        self.assertEqual(bad_response.status_code, 401)

    def test_enrolement_detail(self):
        # add student token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        
        url = reverse('enrolement_create')

        data = {
            'course': self.course.id,
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        enrolement = Enrolment.objects.get(student__id=self.student.id, course=self.course.id)

        url = reverse('enrolement_detail', args=(enrolement.id,))
        response2 = self.client.get(url)

        self.client = APIClient()
        bad_response = self.client.get(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'sample_student@mail.com')
        self.assertEqual(bad_response.status_code, 401)

    def test_enrolement_update(self):
        # add student token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        
        url = reverse('enrolement_create')

        data = {
            'course': self.course.id,
        }

        response1 = self.client.post(url, data=data, content_type='application/json')
        
        enrolement = Enrolment.objects.get(student__id=self.student.id, course=self.course.id)

        url = reverse('enrolement_update', kwargs={'pk': enrolement.pk})
        response2 = self.client.patch(url, data=data, content_type='application/json')

        self.client = APIClient()
        bad_response = self.client.put(url, data=data, content_type='application/json')

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'sample_student@mail.com')
        self.assertEqual(bad_response.status_code, 401)

    def test_enrolement_delete(self):
        # add student token to header
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        
        url = reverse('enrolement_create')

        data = {
            'course': self.course.id,
        }

        response1 = self.client.post(url, data=data, content_type='application/json')        
        
        enrolement = Enrolment.objects.get(student__id=self.student.id, course=self.course.id)

        url = reverse('enrolement_delete', kwargs={'pk': enrolement.pk})
        
        response2 = self.client.delete(url)    
 
        self.client = APIClient()
        bad_response = self.client.delete(url)

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 204)
        self.assertEqual(bad_response.status_code, 401)
