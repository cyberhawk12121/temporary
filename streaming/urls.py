from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('students/', views.student_home, name= 'student_home'),
    path('admin/', views.admin_home, name='admin_home'),
    path('', views.home, name='home'),
    path('register/student', views.StudentSignUpView.as_view(), name='register_student' ),
    path('register/admin', views.AdminSignupView.as_view(), name='register_admin' ),
    path('accounts/login', views.LoginView.as_view(), name='login' ),
    path('accounts/logout', views.logout_view, name='logout' ),
    
    
    path('admin/', include(([

        path('subject/add/', views.SubjectCreateView.as_view(), name='add_subject'),
        path('subject/view/', views.SubjectListView.as_view(), name='view_subject'),
        path('assignment/add/', views.examManagementView.as_view(), name='exam_add1'),
        path('add/questions/<int:id>/', views.add_question, name='question_add1'),
        path('assignment/View/', views.show_assignment, name='show_assignment1'),
        path('assignment/exam/View/<int:id>/', views.show_exam_assignment, name='show_exam_assignment1'),
        path('question/<int:id>', views.delete_question, name='delete_questione1'),
        path('exam/<int:id>', views.delete_assignment, name='delete_assignment1'),
        path('upload/', views.UploadView.as_view(), name='upload'),
        path('show/<id>', views.showvideo, name='show'),
        path('lessons/', views.LessonList.as_view(), name='lesson_list')
        ],'streaming'), namespace='admin')),

    path('students/', include(([
        
        path('assignment/View/', views.show_assignment1, name='show_assignment2'),
        path('assignment/exam/View/<int:id>/', views.show_exam_assignment1, name='show_exam_assignment2'),
        path('assignment/exam/View/result/<int:id>', views.exam_process, name='exam_process1'),
        path('assignment/exam/View/marks/<int:id>', views.exam_result, name= 'result'),
        path('show/<id>', views.showvideo1, name='show1'),
        path('lessons/', views.LessonList1.as_view(), name='lesson_list1')


    ], 'streaming'), namespace= 'student')),  
]