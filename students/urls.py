from django.urls import path

from .views import StudentRegistrationAPIView, StatusUpdateView


urlpatterns = [
    path('register/', StudentRegistrationAPIView.as_view(), name='student_register'),
    path('status/', StatusUpdateView.as_view(), name='status_update'),
]