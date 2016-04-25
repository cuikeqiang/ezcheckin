import time
import datetime

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import models
from .models import Course, Student
    

def student_register(request):
    if request.method == "POST":
        return student_register_post_respond(request)
        
    elif request.method == "GET":
        return student_register_get_respond(request)

    else:
        raise Http404("Question does not exist")

def student_register_post_respond(request):
    number = request.POST.get('student_number', None)
    name = request.POST.get('student_name', None)
    requestTime = request.POST.get('requestTime', None)
    qrcodeTime = request.POST.get('qrcodeTime', None)
    lessonName = request.GET.get('ln', None)
    course = Course.objects.get(pk=lessonName)

    datetimeQrcode = timestamp2datetime(int(qrcodeTime))
    datetimeRequest = timestamp2datetime(int(requestTime))
    print 'time test:'
    print datetimeQrcode, datetimeRequest
    print '----------'

    new_student = course.student_set.create(student_number=number, student_name=name, student_requestTime=datetimeRequest, student_qrcodeTime=datetimeQrcode)
    new_student.save()


    return render(request, "bang/success.html", {'name':name})


def student_register_get_respond(request):        
    timeNow = int(time.time())
    timeQrcode = request.GET.get('time', None)
    timeDifference = timeNow - int(timeQrcode)


    lessonName = request.GET.get('ln', None)
    try:
        Course.objects.get(course_number=lessonName)
    except Course.DoesNotExist:
        course = Course(course_number=lessonName)
        course.save()
    return render(request, "bang/student_register.html", 
        {'requestTime':timeNow, 'qrcodeTime':timeQrcode})

def timestamp2datetime(timestamp, convert_to_local=True):
   ''' Converts UNIX timestamp to a datetime object. '''
   if isinstance(timestamp, (int, long, float)):
       dt = datetime.datetime.utcfromtimestamp(timestamp)
       if convert_to_local:
           dt = dt + datetime.timedelta(hours=8) 
       return dt
   return timestamp

def courses(request):
    # ...
    # output the course name and the the course number
    return render(request, "bang/courses.html", {'coursesList':Course.objects.all()})
    
def course_register(request):
    if request.method == "POST":
        number = request.POST.get('course_number', None)
        name = request.POST.get('course_name', None)
        teacher = request.POST.get('course_teacher', None)
        new_course = Course(course_number=number, course_name=name, course_teacher=teacher)
        new_course.save()
        return render(request, "bang/success.html", {'name':name})
    else:
        return render(request, "bang/course_register.html")

def course_detail(request, course_number):
    # ...
    # course teacher ... and student_name \student_number
    course = Course.objects.get(pk=course_number)
    return render(request, "bang/course_detail.html", {'course':course, 'studentList':Student.objects.all()})
    
