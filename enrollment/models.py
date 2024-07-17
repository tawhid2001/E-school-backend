from django.conf import settings
from django.db import models
from course.models import Course, Lesson


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Ensure a student can enroll in a course only once

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.course_name}"

class LessonProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.OneToOneField(Lesson, related_name='progress', on_delete=models.CASCADE, unique=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} progress on {self.lesson.title}"

