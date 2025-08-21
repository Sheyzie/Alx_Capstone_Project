from rest_framework import generics, views, status, serializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .serializers import InstructorSerializer
from .models import Instructor


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

class InstructorListAPIView(generics.ListAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class InstructorDetailAPIView(generics.RetrieveAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class InstructorDeleteAPIView(generics.DestroyAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def destroy(self, request, pk):
        try:
            instructor = Instructor.objects.get(pk=pk)
        except Instructor.DoesNotExist:
            raise serializers.ValidationError('No instructor exist with that pk')
        
        if hasattr(instructor, 'user'):
            user = instructor.user
        instructor.delete()
        user.delete()
        return Response({'detail': 'Instructor has been deleted.'}, status=200)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def activate_instructor(request, pk):
    try:
        instructor = Instructor.objects.get(pk=pk)
    except Instructor.DoesNotExist:
        raise serializers.ValidationError('No instructor exist with that pk')
    if instructor.status == 'activated':
        return Response({'detail': 'Instructor is already activated.'}, status=200)
    
    instructor.status = 'activated'
    instructor.save()

    return Response({'detail': 'Instructor has been activated.'}, status=200)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def deactivate_instructor(request, pk):
    try:
        instructor = Instructor.objects.get(pk=pk)
    except Instructor.DoesNotExist:
        raise serializers.ValidationError('No instructor exist with that pk')
    if instructor.status == 'deactivated':
        return Response({'detail': 'Instructor is already deactivated.'}, status=200)
    
    instructor.status = 'activated'
    instructor.save()

    return Response({'detail': 'Instructor has been deactivated.'}, status=200)


    

