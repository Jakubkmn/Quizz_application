from django.urls import path
from .views import CustomLoginView, QuizList, QuizDetailView, QuizCreateView, QuizUpdateView, QuizDeleteView, QuestionCreateView, question_change
from django.contrib.auth.views import LogoutView

app_name = 'quiz'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='quiz:login'), name='logout'),
    path('', QuizList.as_view(), name='quizes'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz'),
    path('quiz/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/update/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'),
    path('quiz/<int:pk>/questions/add/', QuestionCreateView.as_view(), name='question-add'),
    path('quiz/<int:pk>/questions/<int:question_pk>/', question_change, name='question-change'),
    path('quiz/delete/<int:pk>/', QuizDeleteView.as_view(), name='quiz-delete'),

    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register_user, name='register'),
    # path('play/', views.play, name='play'),
    # path('create_quiz/', views.create_quiz, name='create_quiz'),
    # path('create_question/<int:quiz_id>/', views.create_question, name='create_question'),
    # path('take_quiz/<int:quiz_id>', views.take_quiz, name='take_quiz'),
    # path('quiz_results/', views.quiz_results, name='quiz_results')

]