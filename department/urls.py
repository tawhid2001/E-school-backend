from django.urls import path,include
from .views import DepartmentViewset,DepartmentCourseViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('list',DepartmentViewset)


urlpatterns = [
    path('',include(router.urls)),
    path('department_courselist/<slug:slug>/',DepartmentCourseViewSet.as_view()),
]
