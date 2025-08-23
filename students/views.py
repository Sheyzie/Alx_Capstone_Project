from rest_framework import generics, status, serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes


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

class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class StudentDetailAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class StudentDeleteAPIView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise serializers.ValidationError('No student exist with that pk')
        
        if hasattr(student, 'user'):
            user = student.user
        student.delete()
        user.delete()
        return Response({'detail': 'Student has been deleted.'}, status=200)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def activate_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        raise serializers.ValidationError('No student exist with that pk')
    if student.status == 'activated':
        return Response({'detail': 'Student is already activated.'}, status=200)
    
    student.status = 'activated'
    student.save()

    return Response({'detail': 'Student has been activated.'}, status=200)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def deactivate_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        raise serializers.ValidationError('No student exist with that pk')
    if student.status == 'deactivated':
        return Response({'detail': 'Student is already deactivated.'}, status=200)
    
    student.status = 'deactivated'
    student.save()

    return Response({'detail': 'Student has been deactivated.'}, status=200)
