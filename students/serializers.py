from rest_framework import serializers
from accounts.serializers import UserSerializer

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # set student status to read only
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'status']