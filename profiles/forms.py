from django import forms

from profiles.models import Student, User
from school.models import Faculty, Course, Grade, ExamResult, Exam


class PostForm(forms.ModelForm):

    class Meta:
        model = ExamResult
        fields = ('exam', 'score',)



