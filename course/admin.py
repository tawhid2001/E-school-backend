from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Lesson)


class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('course_name',),}



admin.site.register(models.Department,DepartmentAdmin)
admin.site.register(models.Course,CourseAdmin)

