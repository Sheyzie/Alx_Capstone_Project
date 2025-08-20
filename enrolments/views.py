from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from instructors.permissions import IsInstructorOrAdmin
from instructors.models import Instructor
from students.models import Student
from students.permissions import IsStudentOrAdmin

from .utils import generate_jitsi_link
from .serializers import CourseSerializer, LessonSerializer, LessonVideoSerializer, EnrolmentSerializer, VideoSessionSerializer
from .models import Course, Lesson, LessonVideo, Enrolment, VideoSession


# ---- COURSE VIEW ----

class CourseCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    filterset_fields = ['title']  # fields for exact filtering

    # Optional: specify search fields
    search_fields = ['title']  # fields to search in

    # Optional: specify ordering fields
    ordering_fields = ['title']  # fields to order by
    ordering = ['title']  # default ordering

class CourseRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer 

class CourseUpdateAPIView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDestroyAPIView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# ---- LESSON VIEW ----

class LessonCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer 

class LessonUpdateAPIView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyAPIView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

# ---- LESSON VIDEO VIEW ----  

class LessonVideoCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer

class LessonVideoListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer

class LessonVideoRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer 

class LessonVideoUpdateAPIView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer

class LessonVideoDestroyAPIView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructorOrAdmin]

    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer

# ---- ENROLMENT VIEW ----  

class EnrolmentCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentOrAdmin]

    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer

    def perform_create(self, serializer):
        # Get the logged-in user
        user = self.request.user

        # Get the related Student object
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student profile not found.")

        # Save the enrollment with student injected
        serializer.save(student=student)

class EnrolmentListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer

class EnrolmentRetrieveAPIView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer 

class EnrolmentUpdateAPIView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentOrAdmin]

    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            student = user.student  # Assuming OneToOneField from User to Student
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=400)

        course_id = request.data.get("course")
        if not course_id:
            return Response({"detail": "Course ID is required."}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=404)

        try:
            enrolement = Enrolment.objects.get(student=student, course=course)
        except Enrolment.DoesNotExist:
            return Response({"detail": "Progress record not found."}, status=404)

        serializer = EnrolmentSerializer(enrolement, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

class EnrolmentDestroyAPIView(DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudentOrAdmin]

    queryset = Enrolment.objects.all()
    serializer_class = EnrolmentSerializer

# ---- VideoSession VIEW ----  
class VideoSessionCreateAPIView(CreateAPIView):
    queryset = VideoSession.objects.all()
    serializer_class = VideoSessionSerializer
    permission_classes = [IsInstructorOrAdmin]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        try:
            instructor = self.request.user.instructor
            course = instructor.course
            session_title = serializer.validated_data.get('session_title')
            
            if not session_title:
                raise serializers.ValidationError("Session title is required to generate the session link.")
            
            session_link = generate_jitsi_link(session_title)
        except AttributeError:
            raise PermissionDenied("User is not an instructor.")
        serializer.save(course=course, instructor=instructor, session_link=session_link)

class VideoSessionListAPIView(ListAPIView):
    queryset = VideoSession.objects.all().order_by('-created_at')
    serializer_class = VideoSessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class VideoSessionRetrieveAPIView(RetrieveAPIView):
    queryset = VideoSession.objects.all()
    serializer_class = VideoSessionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class VideoSessionUpdateAPIView(UpdateAPIView):
    queryset = VideoSession.objects.all()
    serializer_class = VideoSessionSerializer
    permission_classes = [IsInstructorOrAdmin]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        try:
            instructor = self.request.user.instructor
            course = instructor.course
            session_title = serializer.validated_data.get('session_title')
            
            if not session_title:
                raise serializers.ValidationError("Session title is required to generate the session link.")
            
            session_link = generate_jitsi_link(session_title)
        except AttributeError:
            raise PermissionDenied("User is not an instructor.")
        serializer.save(course=course, instructor=instructor, session_link=session_link)

class VideoSessionDeleteAPIView(DestroyAPIView):
    queryset = VideoSession.objects.all()
    serializer_class = VideoSessionSerializer
    permission_classes = [IsInstructorOrAdmin]
    authentication_classes = [JWTAuthentication]

