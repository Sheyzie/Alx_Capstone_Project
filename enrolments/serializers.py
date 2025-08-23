from rest_framework import serializers
from instructors.serializers import InstructorSerializer
from students.serializers import StudentSerializer
from instructors.models import Instructor
from students.models import Student

# to escape html tags
import bleach

from .models import Course, Lesson, LessonVideo, Enrolment, VideoSession


# a list of tags to be allowed in lesson contents
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'code', 'pre'
]

ALLOWED_ATTRIBUTES = {}

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all(), required=False)

    # set status as read only
    # status = serializers.CharField(read_only=True)
    # instructor_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'status']

    def validate(self, attrs):
        request = self.context.get('request')

        if request and request.method == 'PUT' or request.method == 'DELETE':
            # Remove instructor from attrs if present in PUT request
            attrs.pop('instructor', None)

        return attrs
    
    # Make instructor optional on update
    def update(self, instance, validated_data):
        # Remove instructor if not provided in update payload
        if 'instructor' not in validated_data:
            validated_data.pop('instructor', None)
        return super().update(instance, validated_data)

class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)
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

    def validate(self, attrs):
        request = self.context.get('request')

        if request and request.method == 'PUT' or request.method == 'DELETE':
            # Remove course from attrs if present in PUT request
            attrs.pop('course', None)

        return attrs
    
    # Make course optional on update
    def create(self, validated_data):
        request = self.context.get('request')
        user =request.user

        if hasattr(user, 'instructor') and hasattr(user.instructor, 'course'):
            course = user.instructor.course
            validated_data['course'] = course
            lesson = Lesson.objects.create(**validated_data)
            return lesson
        raise serializers.ValidationError('Only intructor can create lessons')

class LessonVideoSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), required=False)

    class Meta:
        model = LessonVideo
        fields = ['lesson', 'url', 'title', 'order']

    def validate(self, attrs):
        request = self.context.get('request')

        if request and request.method == 'PUT' or request.method == 'DELETE':
            # Remove lesson from attrs if present in PUT request
            attrs.pop('lesson', None)

        return attrs
    
    # Make lesson optional on update
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        if hasattr(user, 'instructor') and hasattr(user.instructor, 'course'):
            course = user.instructor.course
            lesson = validated_data.pop('lesson')

            # If lesson came as id (int), fetch it
            if isinstance(lesson, int):
                lesson = Lesson.objects.get(course=course, pk=lesson)

            # (Optional) safety check: make sure this lesson belongs to instructor’s course
            if lesson.course != course:
                raise serializers.ValidationError("This lesson does not belong to your course.")

            lesson_video = LessonVideo.objects.create(lesson=lesson, **validated_data)
            return lesson_video

class EnrolmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)

    # set as read only
    completed = serializers.IntegerField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Enrolment
        fields = ['student', 'course', 'completed', 'date_joined']

    def validate_course(self, value):
        # validate the user isn't already enrolled
        user = self.context['request'].user
        student = getattr(user, 'student', None)

        course = Course.objects.get(pk=value.pk)
        if course.status == 'inactive':
            raise serializers.ValidationError("Course is not active for enrolment.")
        return value
    
    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        student = getattr(user, 'student', None)

        if request and request.method == 'POST':
            if student and Enrolment.objects.filter(student=student, course=attrs['course']).exists():
                raise serializers.ValidationError("Already enrolled in this course.")

        return attrs
    
    # Make increment completed by 1
    def update(self, instance, validated_data):

        instance.completed += 1
        instance.save()
        return instance

class VideoSessionSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(read_only=True)
    instructor = serializers.StringRelatedField(read_only=True)
    session_link = serializers.CharField(read_only=True)
    class Meta:
        model = VideoSession
        fields = ['course', 'instructor', 'session_title', 'scheduled_time', 'session_link']
