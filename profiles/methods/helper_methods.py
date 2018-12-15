from profiles.models import Teacher

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


def grade(midterm, final):
    first = midterm * .40
    second = final * .60
    finalGrade = first + second
    return finalGrade


def get_course_details(courses, student):
    dict =	[]
    totalcal = 0.0
    totalcredit = 0.0
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

    return dict, final_gpa


def find_common_courses(teacher,courses):
    common_courses=[]
    teacher_courses=teacher.courses.all()

    if len(teacher_courses) >= len(courses):
        for s in courses:
            for t in teacher_courses:
                if s==t:
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
            'teacher_faculty': teacher.faculty}
