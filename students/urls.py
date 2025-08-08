from django.urls import path

from .views import StudentRegistrationAPIView


urlpatterns = [
    path('register/', StudentRegistrationAPIView.as_view(), name='student_register'),
]