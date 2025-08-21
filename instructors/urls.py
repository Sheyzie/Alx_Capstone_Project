from django.urls import path

from .views import (
    InstructorRegistrationAPIView, 
    activate_instructor, 
    deactivate_instructor, 
    InstructorListAPIView, 
    InstructorDetailAPIView, 
    InstructorDeleteAPIView
)


urlpatterns = [
    path('', InstructorListAPIView.as_view(), name='instructor_list'),
    path('register/', InstructorRegistrationAPIView.as_view(), name='instructor_register'),
    path('<int:pk>/', InstructorDetailAPIView.as_view(), name='instructor_detail'),
    path('<int:pk>/activate/', activate_instructor, name='instructor_activate'),
    path('<int:pk>/deactivate/', deactivate_instructor, name='instructor_deactivate'),
    path('<int:pk>/delete/', InstructorDeleteAPIView.as_view(), name='instructor_delete'),
]