from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('create_course/', views.create_course, name='create_course'),
    path('course_list/', views.course_list, name='course_list'),
    path('upload_resource/<int:course_id>/', views.upload_resource, name='upload_resource'),
    path('resource_list/<int:course_id>/', views.resource_list, name='resource_list'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('create_assignment/', views.create_assignment, name='create_assignment'),
    path('assignment_list/', views.assignment_list, name='assignment_list'),
    path('student_progress/<int:student_id>/', views.student_progress, name='student_progress'),
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('add_book/', views.add_book, name='add_book'),
    path('book_list/', views.book_list, name='book_list'),
    path('view_books/', views.view_books, name='view_books'),
]
