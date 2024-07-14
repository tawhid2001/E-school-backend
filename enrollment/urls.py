from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, LessonProgressViewSet,CourseProgressView,StudentEnrollmentsView,CourseLessonsWithProgress

router = DefaultRouter()
router.register('enrollments', EnrollmentViewSet)
router.register('lesson-progress', LessonProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('course_progress/<int:course_id>/', CourseProgressView.as_view(), name='course_progress'),
    path('courselessons/<int:pk>/', CourseLessonsWithProgress.as_view(), name="course_lessons_with_progress"),
    path('my-enrollments/', StudentEnrollmentsView.as_view(), name='student-enrollments'),
]
