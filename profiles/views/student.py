
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from profiles.models import Student as stu
from profiles.methods.helper_methods import *


@login_required()
def student_detail(request):
    my_user = request.user
    student = stu.objects.get(user=my_user.pk)
    courses = student.courses.all()

    course_details, final_gpa= get_course_details(courses, student)
    return render(request, 'student_detail.html', {'student': my_user,
                                                   'department': student.department,
                                                   'faculty': student.department.faculty,
                                                   'courses': courses,
                                                   'course_detail_list': course_details,
                                                   'gpa': final_gpa,
                                                   'parent': student.parent
                                                             })



