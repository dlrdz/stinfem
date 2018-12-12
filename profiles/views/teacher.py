from django.http import HttpResponse

from profiles.models import Student, User
from school.models import Faculty, Course, Grade, ExamResult, Exam
from django.shortcuts import render, get_object_or_404

from profiles.forms import PostForm
from django.shortcuts import redirect

def teacher_account(request):
    return render(request, 'teacher/teacher_account.html')

def student_list(request):
    user = User.objects.filter(is_student=True)
    students = user.order_by('last_name')
    return render(request, 'teacher/student_list.html', {'students': students})


def student_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    student = get_object_or_404(Student, user=pk)
    faculty = get_object_or_404(Faculty, departments=student.department)
    courses = student.courses.all()
    dict =	[]
    totalcal = 0.0
    totalcredit = 0.0

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            exam_result = form.save(commit=False)
          #  if student.exams.get(exam=exam_result.exam.pk, student=student.pk):
          #      control = ExamResult.objects.get(exam=exam_result.exam.pk, student=student.pk)
          #      print(control.pk)
          #  print(exam_result.exam.pk)
           # print(student.pk)
            exam_result.student = student
            exam_result.save()

            return student_list(request)
    else:
        form = PostForm()

    for c in courses:
        m = c.exams.get(exam_type="midterm")
        f = c.exams.get(exam_type="f")
        mr = m.results.filter(exam=m.pk, student=student.pk)
        fr = f.results.filter(exam=f.pk, student=student.pk)
        credit=c.credit

        if not mr:
            mid_score=0;
        else:
            mr = mr[0]
            mid_score=mr.score
        if not fr:
            fin_score=0;
        else:
            fr = fr[0]
            fin_score=fr.score

        final_grade = grade(mid_score, fin_score)
        letter_grade = letter(final_grade)


        if(letter_grade == "A"):
            caltimes = float(credit) * 4.0
        elif(letter_grade== "A-" ):
            caltimes = float(credit) * 3.67
        elif(letter_grade == "B+" ):
            caltimes = float(credit) * 3.33
        elif(letter_grade== "B" ):
            caltimes = float(credit) * 3.0
        elif(letter_grade== "B-"):
            caltimes = float(credit) * 2.67
        elif(letter_grade== "C+" ):
            caltimes = float(credit) * 2.33
        elif(letter_grade == "C" ):
            caltimes = float(credit) * 2.0
        elif(letter_grade == "C-" ):
            caltimes = float(credit) * 1.67
        elif(letter_grade == "D" ):
            caltimes = float(credit) * 1.00
        elif(letter_grade == "F" ):
            caltimes = float(credit) * 0.0

        totalcredit = totalcredit + float(credit)
        totalcal = totalcal + caltimes

        x = {'name': c.name,
             'code': c.code,
             'credit': c.credit,
             'midterm': mid_score,
             'final': fin_score,
             'final_grade': final_grade,
             'letter_grade': letter_grade,
             }
        dict.append(x)

    if(totalcredit != 0):
        final_gpa = round(totalcal/totalcredit , 2)
    else:
        final_gpa = "-"

    return render(request, 'teacher/student_detail.html', {'user': user,
                                                           'student': student,
                                                           'faculty': faculty,
                                                           'courses': courses,
                                                           'list': dict,
                                                           'gpa': final_gpa,
                                                           'form': form,
                                                           })


def grade(midterm, final):
    first = midterm * .40
    second = final * .60
    finalGrade = first + second
    return finalGrade

def letter(FinalGrade):
    if FinalGrade >= 94 and FinalGrade <= 100:
        return("A")

    elif FinalGrade >= 90 and FinalGrade < 94:
        return("A-")

    elif FinalGrade >= 87 and FinalGrade < 90:
        return("B+")

    elif FinalGrade >= 84 and FinalGrade < 87:
        return("B")

    elif FinalGrade >= 80 and FinalGrade < 84:
        return("B-")

    elif FinalGrade >= 77 and FinalGrade < 80:
        return("C+")

    elif FinalGrade >= 74 and FinalGrade < 77:
        return("C")

    elif FinalGrade >= 70 and FinalGrade < 74:
        return("C-")

    elif FinalGrade >= 67 and FinalGrade < 70:
        return("D+")

    elif FinalGrade >= 64 and FinalGrade < 67:
        return("D")

    elif FinalGrade >= 61 and FinalGrade < 64:
        return("D-")

    else:
        return("F")

