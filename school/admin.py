from django.contrib import admin

from school.models import Course, Grade, Exam, ExamResult, Department, Faculty

admin.site.register(Course)
admin.site.register(Grade)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Department)
admin.site.register(Faculty)
