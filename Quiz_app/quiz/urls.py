from django.urls import path
from .views import CustomLoginView, QuizList, QuizDetailView, QuizCreateView, QuizUpdateView, QuizDeleteView, QuestionCreateView, question_change, RegisterPage
from django.contrib.auth.views import LogoutView

app_name = 'quiz'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='quiz:login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', QuizList.as_view(), name='quizes'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz'),
    path('quiz/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quiz/update/<int:pk>/', QuizUpdateView.as_view(), name='quiz-update'),
    path('quiz/<int:pk>/questions/add/', QuestionCreateView.as_view(), name='question-add'),
    path('quiz/<int:pk>/questions/<int:question_pk>/', question_change, name='question-change'),
    path('quiz/delete/<int:pk>/', QuizDeleteView.as_view(), name='quiz-delete'),
]