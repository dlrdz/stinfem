from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from profiles.models import Student, User, Teacher
from school.models import Faculty
from profiles.forms import PostForm
from profiles.methods.helper_methods import *
from django.http import HttpResponse, HttpResponseNotFound


@csrf_exempt
def login(request):
    __import__('ipdb').set_trace()
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(email, password)


@login_required()
def teacher_account(request):
    teacher_info=get_teacher_info(request)
    return render(request, 'teacher_account.html', teacher_info)


@login_required()
def student_list(request):
    info = get_teacher_info(request)
    user = User.objects.filter(is_student=True)
    students = user.order_by('last_name')
    info.update({'students':students})
    return render(request, 'student_list.html', info)


@login_required()
def student_detail(request, pk):
    my_user = request.user
    teacher = Teacher.objects.get(user=my_user.pk)
    info=get_teacher_info(request)
    stu_user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Student, user=pk)
    faculty = get_object_or_404(Faculty, departments=student.department)
    courses = student.courses.all()

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            exam_result = form.save(commit=False)
            exam_result.student = student
            exam_result.save()

            return student_list(request)
    else:
        form = PostForm()

    course_details, final_gpa= get_course_details(courses, student)
    common_courses=find_common_courses(teacher,courses)

    info.update({'student': stu_user,
                 'department': student.department,
                 'faculty': faculty,
                 'courses': courses,
                 'course_detail_list': course_details,
                 'gpa': final_gpa,
                 'form': form,
                 'common_courses': common_courses,
                 'parent': student.parent})

    return render(request, 'student_detail.html', info)


