from django.urls import path

from .views import InstructorRegistrationAPIView, StatusUpdateView


urlpatterns = [
    path('register/', InstructorRegistrationAPIView.as_view(), name='instructor_register'),
    path('status/', StatusUpdateView.as_view(), name='status_update'),
]