import time

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import models
from .models import Course, Student
    
def student_register(request):
    if request.method == "POST":
        number = request.POST.get('student_number', None)
        name = request.POST.get('student_name', None)
        lessonName = request.GET.get('ln', None)
        course = Course.objects.get(pk=lessonName)
        new_student = course.student_set.create(student_number=number, student_name=name)
        new_student.save()
        return render(request, "bang/success.html", {'name':name})
    elif request.method == "GET":
        
        timeNow = int(time.time())
        timeQrcode = request.GET.get('time', None)
        timeDifference = timeNow - int(timeQrcode)

        lessonName = request.GET.get('ln', None)
        try:
            Course.objects.get(course_number=lessonName)
            print 'try get course'
        except Course.DoesNotExist:
            course = Course(course_number=lessonName)
            course.save()
            print 'course saved'
        return render(request, "bang/student_register.html")
    else:
        raise Http404("Question does not exist")
    
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
    
