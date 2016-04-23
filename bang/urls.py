from django.conf.urls import url

from . import views

app_name = 'bang'
urlpatterns = [
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/register/$', views.course_register, name='course_register'),
    url(r'^courses/student_register/$', views.student_register, name='student_register'),
    url(r'^courses/(?P<course_number>[a-zA-Z0-9_]+)/$', views.course_detail, name='course_detail'),
]
