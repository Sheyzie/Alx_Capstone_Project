from django.urls import path

from .views import (
    StudentRegistrationAPIView, 
    activate_student, 
    deactivate_student,
    StudentDeleteAPIView,
    StudentDetailAPIView,
    StudentListAPIView
    )


urlpatterns = [
    path('', StudentListAPIView.as_view(), name='student_list'),
    path('register/', StudentRegistrationAPIView.as_view(), name='student_register'),
    path('<int:pk>/', StudentDetailAPIView.as_view(), name='student_detail'),
    path('<int:pk>/activate/', activate_student, name='student_activate'),
    path('<int:pk>/deactivate/', deactivate_student, name='student_deactivate'),
    path('<int:pk>/delete/', StudentDeleteAPIView.as_view(), name='student_delete'),
]