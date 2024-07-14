from django.urls import path,include
from .views import CourseList,CourseDetail,LessonViewSet,LessonDetails,CourseLessons,MyCourseList,LessonListCreate
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('lessons', LessonViewSet)


urlpatterns = [
    path('', CourseList.as_view(),name="course_list"),
    path('<int:course_id>/lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('mycourses/', MyCourseList.as_view(), name='my_course_list'),
    path('<int:pk>/', CourseDetail.as_view(),name="course_detail"),
    path('courselessons/<int:pk>', CourseLessons.as_view(),name="course_lessons"),
    path('<int:pk>/', LessonDetails.as_view(),name="lesson_detail"),
    path('', include(router.urls)),
]
