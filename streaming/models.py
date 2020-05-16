from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from datetime import datetime

class User(AbstractUser):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default=None)
    
    def __str__(self):
        return self.user.firstName + ' ' + self.user.lastName+ ' '+ self.user.username

class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=100,default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    no_question = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_no=models.IntegerField(default=0)
    question = models.TextField(max_length=200,default="")
    option1 = models.CharField(max_length=50,default="")
    option2 = models.CharField(max_length=50, default="")
    option3 = models.CharField(max_length=50, default="")
    option4 = models.CharField(max_length=50, default="")
    answer = models.CharField(max_length=50, default="")
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,default=None)    


    def __str__(self):
        return self.question


class Score(models.Model):
    score= models.IntegerField()
    exam= models.ForeignKey(Exam, on_delete= models.CASCADE)

