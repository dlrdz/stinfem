from django import forms

from profiles.models import Student, User
from school.models import Faculty, Course, Grade, ExamResult, Exam


class PostExamResult(forms.ModelForm):

    class Meta:
        model = ExamResult
        fields = ( 'score',)



