from rest_framework import serializers
from accounts.serializers import UserSerializer

from .models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # set instructor status to read only
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'user', 'status']