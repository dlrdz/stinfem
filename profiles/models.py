from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    parent = models.ForeignKey('profiles.Parent', related_name='students')
    department = models.ForeignKey('school.Department', related_name='students')

    def __str__(self):
        user = self.user
        return (user.first_name +" "+ user.last_name +":  "+ user.email)


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    faculty = models.ForeignKey('school.Faculty', related_name='teachers' )

    def __str__(self):
        user = self.user
        return (user.first_name +" "+ user.last_name +":  "+ user.email)


class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        user = self.user
        return (user.first_name +" "+ user.last_name +":  "+ user.email)
