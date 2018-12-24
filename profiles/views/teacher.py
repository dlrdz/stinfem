from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from profiles.models import Student, User, Teacher
from school.models import Faculty, ExamResult
from profiles.forms import PostExamResult
from profiles.methods.helper_methods import *
from django.http import HttpResponse, HttpResponseNotFound


@csrf_exempt
def login(request):
    __import__('ipdb').set_trace()
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(email, password)

@csrf_exempt
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
def student_detail_teacher(request, pk):
    my_user = request.user
    teacher = Teacher.objects.get(user=my_user.pk)
    info = get_teacher_info(request)
    stu_user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Student, user=pk)
    faculty = get_object_or_404(Faculty, departments=student.department)
    courses = student.courses.all()


    if request.method == "POST":
        form = PostExamResult(request.POST)
        if form.is_valid():
            exam_result = form.save(commit=False)
            exam_result.student = student
            exam_result.save()

            return student_list(request)
    else:
        form = PostExamResult()

    course_details, final_gpa= get_course_details(courses, student)
    common_courses = find_common_courses(teacher, courses)


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


def result_edit(request, pk):
    my_user = request.user
    teacher = Teacher.objects.get(user=my_user.pk)
    examResult = ExamResult.objects.get(pk=pk)
    info=get_teacher_info(request)
    check = False
    for c in teacher.courses.all():
        if c.pk == examResult.exam.course.pk:
            check =True
    if not check:
        return student_list(request)
    post = get_object_or_404(ExamResult, pk=pk)
    if request.method == "POST":
        form = PostExamResult(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return student_list(request)
    else:
        form = PostExamResult(instance=post)

    info.update({'form': form})
    return render(request, 'result_edit.html', info)

