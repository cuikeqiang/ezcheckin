import time
import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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
    student_register_post_create_new_student(request)
    return student_register_post_create_start_page(request)

def student_register_post_create_start_page(request):
    studentNumber = request.POST.get('student_number', None)
    courseNumber = request.GET.get('ln', None)
    return render(request, "bang/student_register_start.html", {'studentNumber':studentNumber, 'courseNumber':courseNumber})

def student_register_post_create_new_student(request):
    number = request.POST.get('student_number', None)
    name = request.POST.get('student_name', None)
    lessonName = request.GET.get('ln', None)
    course = Course.objects.get(pk=lessonName)
    requestTime = request.POST.get('requestTime', None)
    qrcodeTime = request.POST.get('qrcodeTime', None)
    datetimeQrcode = timestamp2datetime(int(qrcodeTime))
    datetimeRequest = timestamp2datetime(int(requestTime))

    try:
        selected_student = course.student_set.get(student_number=number)
    except (KeyError, Student.DoesNotExist):
        new_student = course.student_set.create(student_number=number, student_name=name, student_requestTime=datetimeRequest, student_qrcodeTime=datetimeQrcode, student_heartbeatCount = 0)
        new_student.save()
    else:
        selected_student.student_name = name
        selected_student.student_requestTime = datetimeRequest
        selected_student.student_qrcodeTime = datetimeQrcode
        selected_student.student_heartbeatCount = 0
        selected_student.save()

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
    return render(request, "bang/courses.html", {'coursesList':Course.objects.all()})

@csrf_exempt    
def course_newtable(request, course_number):
    if request.method == "POST":
        course = Course.objects.get(pk=course_number)
        return render(request, "bang/course_newtable.html", {'course':course, 'studentList':Student.objects.all()})
    else:
        raise Http404("Question does not exist")

@csrf_exempt  
def course_heartbeat(request):
    if request.method == "POST":
        heartBeatCount = course_heartbeat_get_heartbeat_count(request)
        return HttpResponse(heartBeatCount)
    else:
        raise Http404("Question does not exist")

def course_heartbeat_get_heartbeat_count(request):
    
    course_number = request.POST.get('course_number', None)
    course = Course.objects.get(pk=course_number)
    number = request.POST.get('student_number', None)   
    try:  
        selected_student = course.student_set.get(student_number=number)
    except (KeyError, Student.DoesNotExist):
        raise Http404("Question does not exist")
    else:
        selected_student.student_heartbeatCount += 1
        selected_student.save()
        return selected_student.student_heartbeatCount




def course_detail(request, course_number):
    course = Course.objects.get(pk=course_number)
    return render(request, "bang/course_detail.html", {'course':course, 'studentList':Student.objects.all()})
    
