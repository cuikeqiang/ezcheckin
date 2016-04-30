from django.conf.urls import url

from . import views

app_name = 'bang'
urlpatterns = [
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^courses/student_register/$', views.student_register, name='student_register'),
    url(r'^courses/(?P<course_number>[a-zA-Z0-9_]+)/$', views.course_detail, name='course_detail'),
    url(r'^courses/(?P<course_number>[a-zA-Z0-9_]+)/newtable/$', views.course_newtable, name='course_newtable'),
    url(r'^courses/student_register/heartbeat/$', views.course_heartbeat, name='course_heartbeat'),
]

