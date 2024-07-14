from rest_framework import serializers
from . import models
from course.models import Course

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LessonProgress
        fields = '__all__'


class ProgressSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    course_name = serializers.CharField()
    progress = serializers.FloatField()