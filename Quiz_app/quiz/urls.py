from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('play/', views.play, name='play'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('create_questions/<int:quiz_id>/<int:question_id>/', views.create_question, name='create_question'),
    path('take_quiz/<int:quiz_id>', views.take_quiz, name='take_quiz'),
    path('quiz_results/', views.quiz_results, name='quiz_results')

]