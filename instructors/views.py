from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import InstructorSerializer
from .models import Instructor


User = get_user_model()

class InstructorRegistrationAPIView(generics.CreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # deactivate the instructor status
        instructor = serializer.save()
        instructor.status = 'deactivated'
        instructor.save()

        # ensure that role = instructor
        if hasattr(instructor.user, 'profile'):
            instructor.user.profile.role = 'instructor'
            instructor.user.profile.save()

        # create linked instructor model
        # Instructor.objects.create(user=user, status='deactivated')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
