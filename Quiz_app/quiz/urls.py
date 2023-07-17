from django.urls import path
from .views import CustomLoginView, QuizList, QuizDetailView, QuizCreateView

app_name = 'quiz'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', QuizList.as_view(), name='quizes'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz'),
    path('quiz-create/', QuizCreateView.as_view(), name='quiz-create')

    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),
    # path('play/', views.play, name='play'),
    # path('create_quiz/', views.create_quiz, name='create_quiz'),
    # path('create_question/<int:quiz_id>/', views.create_question, name='create_question'),
    # path('take_quiz/<int:quiz_id>', views.take_quiz, name='take_quiz'),
    # path('quiz_results/', views.quiz_results, name='quiz_results')

]