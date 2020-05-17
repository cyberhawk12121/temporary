from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, Http404
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, request, HttpResponseRedirect, HttpResponseBadRequest 
from django.utils.decorators import method_decorator
import datetime


from django.views.generic import (
    TemplateView, 
    View, 
    CreateView, 
    DeleteView, 
    DetailView, 
    ListView,
    UpdateView
    )

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignupForm
    template_name = 'streaming/student_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Student.objects.create(user=user)
        login(self.request, user)
        return redirect('student_home')

class AdminSignupView(CreateView):
    model = User
    form_class = AdminSignupForm
    template_name = 'streaming/admin_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Admin.objects.create(user=user)
        login(self.request, user)
        return redirect('admin_home')


class LoginView(TemplateView):
    template_name= 'streaming/login.html'
    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect('home')
        # else:
        form= LoginForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        if request.POST:
            form= LoginForm(request.POST)
            if form.is_valid():
                username= form.cleaned_data.get('username')
                password= form.cleaned_data.get('password')
                print(username, password)
                user= authenticate(username= username, password= password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        else:
            form= LoginForm()
        return render(request, self.template_name, {'form':form})

def home(request):
    if request.user.is_authenticated:
        if request.user.is_student:
            return redirect('student_home')
        else:
            return redirect('admin_home')

    return render(request, 'streaming/index.html')

@login_required
@student_required
def student_home(request):
    return render(request, 'streaming/student_home.html')

@admin_required
@login_required
def admin_home(request):
    return render(request, 'streaming/admin_home.html')

def logout_view(request):
    logout(request)
    return redirect('home')



""" ================ ONLY FOR ADMIN ================= """

@method_decorator([login_required, admin_required], name='dispatch')
class SubjectCreateView(CreateView):
    model = Subject
    fields = ('name', 'color',)
    template_name = 'streaming/subject_add_form.html'

    def form_valid(self, form):
        subject = form.save(commit=False)
        subject.save()
        messages.success(self.request, 'Subject created successfully!')
        return redirect('admin:home')
        
@method_decorator([login_required, admin_required], name='dispatch')
class SubjectListView(ListView):
    model = Subject
    template_name = 'streaming/subjects.html'

    def get_context_data(self, **kwargs):
        subjects= Subject.objects.all()
        return {'subjects': subjects}



class examManagementView(CreateView, LoginRequiredMixin):
    model= Exam
    form_class= ExamAddForm
    template_name= 'streaming/add_assignment.html'
    def form_valid(self,form):
        # user= self.request.user
        name= form.cleaned_data['name']
        subject= form.cleaned_data['subject']
        no_question=form.cleaned_data['no_question']
        print(name, subject, no_question)
        form.save()
        return redirect('admin:show_assignment1')


def add_question(request,id):
    ids = id
    exam_obj= Exam.objects.get(id=ids)
    question_no=Question.objects.filter(exam=exam_obj).count()
    question=Question.objects.filter(exam=exam_obj).count()+question_no+1
    print("Number of questions right now: ",question_no)
    
    if exam_obj.no_question > question_no:
        exam = Exam.objects.all()
        form = AddQuestionForm(request.POST or None)
        if request.method == 'POST':
            form = AddQuestionForm(request.POST or None)
        if form.is_valid():
            form.save(id)
            form = AddQuestionForm()
    else:
        return redirect('admin:show_assignment1')
    return render(request,'streaming/question_add_form.html',{'form':form,'exam':exam,'ids':ids,'question':question})


def show_assignment(request):
    print(datetime.time())
    assignments = Exam.objects.all()
    return render(request,'streaming/show_exam.html',{'assignments':assignments})

def show_exam_assignment(request,id):
    assignments = Exam.objects.all()
    exam= Exam.objects.get(id=id)
    questions = Question.objects.filter(exam=exam)
    # question_no=Question.objects.filter(exam=exam).values('question').count()
    ids = id
    exam= Exam.objects.filter(id=id)
    return render(request, 'streaming/show_exam_assignment.html', {'assignments': assignments,'questions': questions,'ids':ids})

def delete_question(request,id):
    question = Question.objects.filter(id=id)
    question.delete()
    return HttpResponseRedirect('/admin/assignment/View/')

def delete_assignment(request,id):
    exam = Exam.objects.filter(id=id)
    exam.delete()
    return HttpResponseRedirect('/admin/assignment/View/')   
    
class UploadView(CreateView):
    model= Lesson
    form_class= UploadForm
    template_name= 'streaming/upload.html'
    def form_valid(self, form):
        form.save()
        return redirect('home')

class LessonList(ListView):
    model= Lesson
    template_name= 'streaming/lesson_list.html'
    def get_context_data(self, **kwargs):
        lesson= Lesson.objects.all()
        return {'lesson': lesson}


def showvideo(request, id):
    lastvideo= Lesson.objects.get(id=id)
    videofile= lastvideo.video
    context= {'videofile': videofile,}
    print(videofile)
    return render(request, 'streaming/show_video.html', context)






""" ============================ ONLY FOR STUDENTS ============================== """
def show_assignment1(request):
    # user= User.objects.get(username=request.user)
    student=Student.objects.get(user=request.user)
    assignments = Exam.objects.all()
    return render(request,'streaming/show_exam_student.html',{'assignments':assignments})

def show_exam_assignment1(request,id):
    exam= Exam.objects.get(id=id)
    ids= id
    if Score.objects.filter(exam=exam):
        message= "You have submitted your test already."
        context= {
            'message':message,
            'id': ids
        }
        return render(request,'streaming/test_error.html', context)
    else:
        assignments= Exam.objects.all()
        questions = Question.objects.filter(exam=id)
        ids = id
        print(assignments)
        return render(request, 'streaming/show_exam_assignment_student.html', {'assignments': assignments,'questions': questions,'ids':ids})

def exam_process(request, id):
    if request.POST:
        exam= Exam.objects.get(id=id)
        ids= id
        if Score.objects.filter(exam=exam):
            message= "You have submitted your test already."
            context= {
                'message':message,
                'id': ids
            }
            return render(request,'streaming/test_error.html', context)
        else:
            question_set= Question.objects.all()
            form_response= request.POST.copy()
            score=0
            for question in question_set:
                if question.answer == form_response.get('choice'+str(question.question_no)):
                    score+=1
                else:
                    continue 
            exam= Exam.objects.get(id=id)
            score_obj= Score.objects.create(exam=exam, score=score)
            ids = id
            score_obj.save()
        return render(request, 'streaming/exam_success.html', {'score':score})

def exam_result(request, id):
    exam= Exam.objects.get(id=id)
    ids = id
    score= Score.objects.filter(exam=exam)
    return render(request, 'streaming/exam_result.html', {'score':score})

class LessonList1(ListView):
    model= Lesson
    template_name= 'streaming/lesson_list_student.html'
    def get_context_data(self, **kwargs):
        lesson= Lesson.objects.all()
        return {'lesson': lesson}


def showvideo1(request, id):
    lastvideo= Lesson.objects.get(id=id)
    videofile= lastvideo.video
    context= {'videofile': videofile,}
    print(videofile)
    return render(request, 'streaming/show_video_student.html', context)






    





