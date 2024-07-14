from rest_framework import serializers
from .models import Course,Lesson



class CourseListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_code', 'description', 'created_at', 'slug', 'teacher', 'teacher_name', 'department', 'department_name']

        read_only_fields = ["teacher",]

    def get_teacher_name(self, obj):
        return obj.teacher.get_full_name() or obj.teacher.username

    def get_department_name(self, obj):
        return obj.department.name

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'