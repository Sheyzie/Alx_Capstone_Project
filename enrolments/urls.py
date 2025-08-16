from django.urls import path

from . import views


urlpatterns = [
    # --- Course Route ---
    path('courses/', views.CourseListAPIView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateAPIView.as_view(), name='course_create'),
    path('courses/<int:pk>/', views.CourseRetrieveAPIView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', views.CourseUpdateAPIView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDestroyAPIView.as_view(), name='course_delete'),

    # --- Lesson Route ---
    path('lessons/', views.LessonListAPIView.as_view(), name='lesson_list'),
    path('lessons/create/', views.LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/edit/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),

    # --- Lesson Video Route ---
    path('lesson-videos/', views.LessonVideoListAPIView.as_view(), name='lesson_video_list'),
    path('lesson-videos/create/', views.LessonVideoCreateAPIView.as_view(), name='lesson_video_create'),
    path('lesson-videos/<int:pk>/', views.LessonVideoRetrieveAPIView.as_view(), name='lesson_video_detail'),
    path('lesson-videos/<int:pk>/edit/', views.LessonVideoUpdateAPIView.as_view(), name='lesson_video_update'),
    path('lesson-videos/<int:pk>/delete/', views.LessonVideoDestroyAPIView.as_view(), name='lesson_video_delete'),

    # --- Enrolment Route ---
    path('enrolments/', views.EnrolmentListAPIView.as_view(), name='enrolement_list'),
    path('enrolments/create/', views.EnrolmentCreateAPIView.as_view(), name='enrolement_create'),
    path('enrolments/<int:pk>/', views.EnrolmentRetrieveAPIView.as_view(), name='enrolement_detail'),
    path('enrolments/<int:pk>/edit/', views.EnrolmentUpdateAPIView.as_view(), name='enrolement_update'),
    path('enrolments/<int:pk>/delete/', views.EnrolmentDestroyAPIView.as_view(), name='enrolement_delete'),
]