from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from .models import Course,Lesson
from .serializers import CourseListSerializer,LessonSerializer
from django.http import Http404
# from .permissions import IsTeacherrOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CourseList(APIView):
    # permission_classes = [IsTeacherrOrReadOnly]
    def get(self,request,format=None):
        user = request.user
        if user.user_type == 'teacher':
            courses = Course.objects.filter(teacher=user)
        else:
            courses = Course.objects.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = CourseListSerializer(data=request.data)
        data = request.data
        data['teacher'] = request.user.id
        serializer.teacher = request.user
        if serializer.is_valid():
            serializer.save(teacher = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class MyCourseList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if user.user_type == 'teacher':
            courses = Course.objects.filter(teacher=user)
            serializer = CourseListSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

class CourseDetail(APIView):
    # permission_classes = [IsTeacherrOrReadOnly]
    def get_object(self,pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        course = self.get_object(pk)
        serializer = CourseListSerializer(course)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        course = self.get_object(pk)
        serializer = CourseListSerializer(course,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        course =self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class LessonViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsTeacherrOrReadOnly]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonListCreate(APIView):
    def get(self, request, course_id, format=None):
        lessons = Lesson.objects.filter(course_id=course_id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request, course_id, format=None):
        data = request.data
        data['course'] = course_id
        serializer = LessonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonDetails(APIView):
    def get_object(self,pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,format=None):
        lesson =self.get_object(pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
   

    def get_lessons_in_course(self, course_id):
        lessons = Lesson.objects.filter(course_id=course_id)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)   


class CourseLessons(APIView):
    # permission_classes = [IsTeacherrOrReadOnly]
    def get(self, request, pk, format=None):
        course = Course.objects.get(pk=pk)
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons,many=True)
        return Response(serializer.data)