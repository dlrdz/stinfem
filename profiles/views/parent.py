from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from profiles.models import User
from school.models import Faculty
from profiles.methods.helper_methods import *
from profiles.models import Student, Parent


@login_required()
def student_list(request):
    my_user = request.user
    parent = Parent.objects.get(user=my_user.pk)
    students = parent.students.all()
    dict=[]
    for s in students:
        user= s.user
        dict.append(user)

    return render(request, 'student_list.html', {'students': dict})



@login_required()
def student_detail(request, pk):
    my_user = request.user
    stu_user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Student, user=pk)
    faculty = get_object_or_404(Faculty, departments=student.department)
    courses = student.courses.all()

    course_details, final_gpa= get_course_details(courses, student)

    return render(request, 'student_detail.html', {'student': stu_user,
                                                   'department': student.department,
                                                   'faculty': faculty,
                                                   'courses': courses,
                                                   'course_detail_list': course_details,
                                                   'gpa': final_gpa,
                                                   'parent': student.parent})



