from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Enrollment,LessonProgress
from course.models import Course
from .serializers import EnrollmentSerializer,LessonProgressSerializer,ProgressSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        student = self.request.user
        return Enrollment.objects.filter(student=student)
    
    def create(self, request, *args, **kwargs):
        student = request.user
        course_id = request.data.get('course')
        if Enrollment.objects.filter(student=student, course_id=course_id).exists():
            return Response({'detail': 'Already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)
        data = {'student': student.id, 'course': course_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

class LessonProgressViewSet(viewsets.ModelViewSet):
    queryset = LessonProgress.objects.all()
    serializer_class = LessonProgressSerializer


class CourseLessonsWithProgress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        lessons = course.lessons.all()
        user = request.user

        lessons_data = []
        for lesson in lessons:
            progress = LessonProgress.objects.filter(lesson=lesson, student=user).first()
            lesson_data = {
                'id': lesson.id,
                'title': lesson.title,
                'content': lesson.content,
                'created_at': lesson.created_at,
                'completed': progress.completed if progress else False,
            }
            lessons_data.append(lesson_data)

        return Response(lessons_data)

class CourseProgressView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        total_lessons = course.lessons.count()
        if total_lessons == 0:
            progress_percentage = 0
        else:
            completed_lessons = LessonProgress.objects.filter(student=user, lesson__course=course, completed=True).count()
            progress_percentage = (completed_lessons / total_lessons) * 100

        progress_data = {
            'course_id': course.id,
            'course_name': course.course_name,
            'progress': progress_percentage
        }

        serializer = ProgressSerializer(progress_data)
        return Response(serializer.data)
    

class StudentEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student = request.user
        enrollments = Enrollment.objects.filter(student=student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)