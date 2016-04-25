from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
    """
    the course class
    """
    course_number = models.CharField(max_length=80, primary_key=True)
    course_name = models.CharField(max_length=800)
    course_teacher = models.CharField(max_length=80)

    
    def __unicode__(self):
        return self.course_number + '  :  ' + self.course_name + '  :  ' + self.course_teacher

class Student(models.Model):
    """
    the student class
    """
    # donot understand on_delete
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    student_number = models.CharField(max_length=40)
    student_name = models.CharField(max_length=40)
    student_requestTime = models.DateTimeField('time that student sent the request')
    student_qrcodeTime = models.DateTimeField('time that qrcode generated')
    
    # should add date
    def __unicode__(self):
        return self.student_number + '  :  ' + self.student_name
        
    # add some method to verify the student_number
        


    
    
    
