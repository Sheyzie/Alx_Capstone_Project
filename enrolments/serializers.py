from rest_framework import serializers
from instructors.serializers import InstructorSerializer
from students.serializers import StudentSerializer

# to escape html tags
import bleach

from .models import Course, Lesson, LessonVideo, Enrolment


# a list of tags to be allowed in lesson contents
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'code', 'pre'
]

ALLOWED_ATTRIBUTES = {}

class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer()

    # set status as read only
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'status']


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'order', 'created_at', 'updated_at']

    # validate content to screen for html tags
    def validate_content(self, value):
        return bleach.clean(
            value,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )


class LessonVideoSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = LessonVideo
        fields = ['lesson', 'url', 'title', 'order']


class EnrolmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    course = CourseSerializer()

    # set as read only
    completed = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Enrolment
        fields = ['student', 'course', 'completed', 'date_joined']
