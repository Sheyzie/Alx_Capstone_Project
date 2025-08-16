from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile


User = get_user_model()

# serializer for user profile
class UserProfileSerializer(serializers.ModelSerializer):
    # set role as read-only
    role = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'role']

# serializer for user
class UserSerializer(serializers.ModelSerializer):
    # include the serializer for user profile
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'profile']

        # set password as write only
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # extract profile data and password from validated
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')

        # creating user instance
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        request = self.context.get('request')
        path = request.path if request else ""
        
        # Infer role from URL path
        if 'instructor' in path:
            role = 'instructor'
        elif 'student' in path:
            role = 'student'
        else:
            role = 'student'  # Default fallback
        
        # create the profile for user
        UserProfile.objects.create(user=user, role=role, **profile_data)
        return user