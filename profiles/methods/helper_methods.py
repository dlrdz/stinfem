from profiles.models import Teacher
from school.models import ExamResult, Exam



def find_letter_grade(FinalGrade):
    try:
        FinalGrade = int(FinalGrade)
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
    except ValueError:
        return ("IP")


def calculate_final_grade(midterm, final):
    try:
        midterm = int(midterm)
        first = midterm * .40
        second = final * .60
        finalGrade = round(first + second, 2)
    except ValueError:
        finalGrade = "IP"
    return finalGrade


def calculate_gpa(courses):
    total_score = 0.0
    total_credit = 0.0
    score = 0.0

    for c in courses:
        if(c["letter_grade"] == "A"):
            score = float(c["credit"]) * 4.0
        elif(c["letter_grade"] == "A-" ):
            score = float(c["credit"]) * 3.67
        elif(c["letter_grade"] == "B+" ):
            score = float(c["credit"]) * 3.33
        elif(c["letter_grade"] == "B" ):
            score = float(c["credit"]) * 3.0
        elif(c["letter_grade"] == "B-"):
            score = float(c["credit"]) * 2.67
        elif(c["letter_grade"] == "C+" ):
            score = float(c["credit"]) * 2.33
        elif(c["letter_grade"] == "C" ):
            score = float(c["credit"]) * 2.0
        elif(c["letter_grade"] == "C-" ):
            score = float(c["credit"]) * 1.67
        elif(c["letter_grade"] == "D" ):
            score = float(c["credit"]) * 1.00
        elif(c["letter_grade"] == "F" ):
            score = float(c["credit"]) * 0.0
        elif(c["letter_grade"] == "IP" ):
            return "-"

        total_credit = total_credit + float(c["credit"])
        total_score = total_score + score

    if(total_credit != 0 and total_score != 0):
        final_gpa = round(total_score/total_credit, 2)
    else:
        final_gpa = "-"

    return final_gpa


def get_course_details(courses, student):
    dict =	[]
    totalcal = 0.0
    totalcredit = 0.0
    caltimes=0

    for c in courses:

        if not c.exams.all():
            Exam.objects.create(exam_type="f", course=c)
            Exam.objects.create(exam_type="midterm", course=c)
            m = c.exams.get(exam_type="midterm")
            f = c.exams.get(exam_type="f")
            ExamResult.objects.create(exam=m, student=student, score=999)
            mid_score= 999;
            mid__pk = m.results.filter(exam=m, student=student)[0].pk
            ExamResult.objects.create(exam=f, student=student, score=999)
            fin_score=999;
            fin__pk = m.results.filter(exam=f, student=student)[0].pk

        m = c.exams.get(exam_type="midterm")
        f = c.exams.get(exam_type="f")
        mr = m.results.filter(exam=m.pk, student=student.pk)
        fr = f.results.filter(exam=f.pk, student=student.pk)

        if not mr:
            ExamResult.objects.create(exam=m, student=student, score=999)
            mid_score= 999;
            mid__pk = m.results.filter(exam=m, student=student)[0].pk
        else:
            mr = mr[0]
            mid_score = mr.score
            mid__pk = mr.pk
        if not fr:
            ExamResult.objects.create(exam=f, student=student, score=999)
            fin_score=999;
            fin__pk = m.results.filter(exam=f, student=student)[0].pk

        else:
            fr = fr[0]
            fin__pk = fr.pk
            fin_score= fr.score

        if mid_score < 0:
            mid_score = 0
            if 0 <= fin_score <= 100:
                final_grade = calculate_final_grade(mid_score, fin_score)
                letter_grade = find_letter_grade(final_grade)

        if mid_score > 100:
            mid_score= "IP"
            final_grade = "IP"
            letter_grade = "IP"
        if fin_score > 100:
            fin_score= "IP"
            final_grade = "IP"
            letter_grade = "IP"
        elif fin_score < 0:
            fin_score= "X"
            final_grade="X"
            letter_grade="F"
        else:
            final_grade = calculate_final_grade(mid_score, fin_score)
            letter_grade = find_letter_grade(final_grade)


        x = {'course': c,
            'name': c.name,
             'code': c.code,
             'credit': c.credit,
             'midterm': mid_score,
             'mid_pk': mid__pk,
             'final': fin_score,
             'fin_pk': fin__pk,
             'final_grade': final_grade,
             'letter_grade': letter_grade,
             'course_pk': c.pk,
             }
        dict.append(x)

    final_gpa = calculate_gpa(dict)
    return dict, final_gpa


def find_common_courses(teacher, courses):
    common_courses=[]
    teacher_courses=teacher.courses.all()

    if len(teacher_courses) >= len(courses):
        for s in courses:
            for t in teacher_courses:
                if s == t:
                    common_courses.append(t)


    elif len(teacher_courses) < len(courses):
        for t in teacher_courses:
            for s in courses:
                if t==s:
                    common_courses.append(s)

    return common_courses


def get_teacher_info(request):
    my_user = request.user
    teacher = Teacher.objects.get(user=my_user.pk)
    return {'teacher': my_user,
            'teacher_faculty': teacher.faculty,
            'teacher_courses': teacher.courses.all()}
