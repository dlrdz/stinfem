from django.conf.urls import url
from profiles.views import teacher, student, parent

urlpatterns = [
    url(r'^student/$', student.student_detail, name='student_main_page'),
    url(r'^parent/$', parent.student_list, name='parent_main_page'),
    url(r'^parent/(?P<pk>[0-9]+)/$', parent.student_detail, name='detail_for_parent'),
    url(r'^teacher/$', teacher.teacher_account, name='teacher_main_page'),
    url(r'^teacher/list/$', teacher.student_list, name='student_list'),
    url(r'^(?P<pk>[0-9]+)/$', teacher.student_detail_teacher, name='detail'),
    url(r'^result/(?P<pk>[0-9]+)/edit$', teacher.result_edit, name='result_edit'),
]
