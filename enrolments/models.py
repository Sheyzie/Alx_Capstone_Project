from django.db import models
from instructors.models import Instructor
from students.models import Student

# to support html tags
# from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field

# to allow specific html tags
import bleach

# a list of tags to be allowed in lesson contents
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'code', 'pre'
]

ALLOWED_ATTRIBUTES = {}

class Course(models.Model):
    STATUS_CHOICE = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    instructor = models.OneToOneField(Instructor, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, through='Enrolment', related_name='course')
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')
    title = models.CharField(max_length=255)
    content = CKEditor5Field('Text', config_name='extends') 
    order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # modifying the save method to screen for tags with bleach
    def save(self, *args, **kwargs):
        # sanitize contents before saving
        self.content = bleach.clean(
            self.content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True
        )
        super().save(*args, **kwargs)

class LessonVideo(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='videos')
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=1)



class Enrolment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolment')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolment')
    completed = models.PositiveSmallIntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # prevent duplicate enrollments

