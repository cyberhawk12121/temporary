from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms import formset_factory
from .models import *


class StudentSignupForm(UserCreationForm):
    firstName = forms.CharField(label='First Name:', widget=forms.TextInput(attrs={'class':'form-control'}))
    lastName = forms.CharField(label='Last Name:', widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Retype Password:', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = User
        field= ('firstName', 'lastName')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class AdminSignupForm(UserCreationForm):
    
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Retype Password:', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username= forms.CharField(max_length=255, widget= forms.TextInput(attrs={'class':'form-control'}))
    password= forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control'}))



# Online Test
class ExamAddForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('subject','name','no_question')
        widgets = {
            'no_question': forms.NumberInput(attrs={'min':1 ,'max':20, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question','option1','option2','option3','option4','answer')
        widgets= {
            'question': forms.Textarea(attrs={'class':'form-control'}),
            'option1': forms.TextInput(attrs={'class':'form-control'}),
            'option2': forms.TextInput(attrs={'class':'form-control'}),
            'option3': forms.TextInput(attrs={'class':'form-control'}),
            'option4': forms.TextInput(attrs={'class':'form-control'}),
            'answer': forms.TextInput(attrs={'class':'form-control'})
        }
    def save(self, id):
        exam= Exam.objects.get(id=id)
        question = self.cleaned_data['question']
        option1 = self.cleaned_data['option1']
        option2 = self.cleaned_data['option2']
        option3 = self.cleaned_data['option3']
        option4 = self.cleaned_data['option4']
        answer = self.cleaned_data['answer']

        question= Question.objects.create(question=question, option1=option1,
                            option2=option2, option3=option3,
                            option4=option4,answer=answer,exam=exam)
        question.question_no = Question.objects.values('question_no').count()+1
        question.save()


        
    