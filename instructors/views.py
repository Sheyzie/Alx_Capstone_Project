from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer

from .models import Instructor


User = get_user_model()

class InstructorRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # invoke UserSerializer.create(validated_data) implemented in accounts.serializer
        user = serializer.save()

        # ensure that role = instructor
        if hasattr(user, 'profile'):
            user.profile.role = 'instructor'
            user.profile.save()

        # create linked instructor model
        Instructor.objects.create(user=user, status='deactivated')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
