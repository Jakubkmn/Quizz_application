from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
# from .forms import SignUpForm, QuizForm, QuestionForm, AnswerForm
from .models import Quiz, Question, Answer


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'quiz/login.html'
    fiels = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('quizes')

class QuizList(ListView):
    model = Quiz
    context_object_name = 'quizes'

class QuizDetailView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/quiz.html'

class QuizCreateView(CreateView):
    model = Quiz
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('quizes')

