from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    credit = models.PositiveIntegerField()
    teachers = models.ManyToManyField('profiles.Teacher', related_name='courses')
    students = models.ManyToManyField('profiles.Student',
                                      through='Grade',
                                      related_name='courses')

    def __str__(self):
        return self.code


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('school.Faculty', related_name='departments')

    def __str__(self):
        return self.name


class Grade(models.Model):
    # Connection table betweeb student and subject
    student = models.ForeignKey('profiles.Student')
    course = models.ForeignKey(Course, related_name='grades')
    grade = models.CharField(max_length=10)

    def __str__(self):
        return (self.course.code + ": " + self.student.user.first_name+ " " + self.student.user.last_name)



class Exam(models.Model):
    TYPE = (
        ('midterm', 'Midterm'),
        ('f', 'Final')
    )
    course = models.ForeignKey(Course, related_name='exams')
    student = models.ManyToManyField('profiles.Student',
                                     through='ExamResult',
                                     related_name='exams')
    exam_type = models.CharField(choices=TYPE, max_length=50)

    def __str__(self):
        return (self.course.name + ": " + self.exam_type)


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, related_name='results')
    student = models.ForeignKey('profiles.Student',
                                related_name='exam_results')
    score = models.IntegerField(default=999)

    def __str__(self):
        return (self.student.user.first_name +": "+ self.exam.course.name + " " + self.exam.exam_type )


