from django.db import models
from django.conf import settings


class Instructor(models.Model):
    STATUS_CHOICE = [
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor')
    status = models.CharField(max_length=12, choices=STATUS_CHOICE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} (Instructor)'
