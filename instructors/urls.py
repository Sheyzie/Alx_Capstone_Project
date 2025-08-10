from django.urls import path

from .views import InstructorRegistrationAPIView


urlpatterns = [
    path('register/', InstructorRegistrationAPIView.as_view(), name='instructor_register'),
]