from rest_framework import serializers
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from accounts.models import UserProfile

from .models import Instructor


User = get_user_model()

class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # set instructor status to read only
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Instructor
        fields = ['id', 'user', 'status']

    # Custome create method
    def create(self, validated_data):
        # Extract nested user data
        user_data = validated_data.pop('user')
        user_profile_data = user_data.pop('profile')

        # Creating user
        user = User.objects.create_user(**user_data)
        user.profile = UserProfile.objects.create(user=user, **user_profile_data)

        user.profile.role = 'instructor'
        user.profile.save()
        user.save()

        # Now create the instructor and link the user
        instructor = Instructor.objects.create(user=user, **validated_data)

        return instructor