from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'

    def get_success_url(self, request, user):
        if user.is_teacher:
            redirect_to = settings.TEACHER_REDIRECT_URL
        if user.is_student:
            redirect_to = settings.STUDENT_REDIRECT_URL
        if user.is_parent:
            redirect_to = settings.PARENT_REDIRECT_URL
        return reverse(redirect_to)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            data = form.data
            print(data)
            username, password = data.get('username'), data.get('password')
            print(username, password)
            user = authenticate(username=username, password=password)
            print(user)
            login(request, user)
            return HttpResponseRedirect(self.get_success_url(request, user))
        else:
            return self.form_invalid(form)
