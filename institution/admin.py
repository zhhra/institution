from django.contrib import admin
from .models import Classroom,TheClass,Student,Teacher,Lesson
# Register your models here.

admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(TheClass)
admin.site.register(Student)
admin.site.register(Lesson)
