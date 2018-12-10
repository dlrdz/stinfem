from django.conf.urls import url
from profiles.views import teacher

urlpatterns = [
    url(r'^teacher/$', teacher.student_list, name='student_list'),
    url(r'^(?P<pk>[0-9]+)/$', teacher.student_detail, name='detail'),


]
