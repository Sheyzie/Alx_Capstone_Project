from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .serializers import StudentSerializer
from .models import Student


class StudentRegistrationAPIView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # activate student status
        student = serializer.save()
        student.status = 'activated'
        student.save()

        # ensure that role = student
        if hasattr(student.user, 'profile'):
            student.user.profile.role = 'student'
            student.user.profile.save()

        # create linked student model
        # Student.objects.create(user=user, status='activated')

        return Response(serializer.data, status=status.HTTP_201_CREATED)
