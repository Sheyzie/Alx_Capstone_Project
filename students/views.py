from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

from .models import Student


User = get_user_model()

class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # invoke UserSerializer.create(validated_data) implemented in accounts.serializer
        user = serializer.save()

        # ensure that role = student
        if hasattr(user, 'profile'):
            user.profile.role = 'student'
            user.profile.save()

        # create linked student model
        Student.objects.create(user=user, is_active=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
