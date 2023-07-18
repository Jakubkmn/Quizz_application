from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return redirect('quiz-update', quiz.pk)
    
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = '__all__'
    success_url = reverse_lazy('quiz:quizes')

class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    success_url = reverse_lazy('quiz:quizes')

class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']

    def get_context_data(self, **kwargs):
        data = super.get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = forms.formset_factory(QuestionForm, extra=self.kwargs['questions_count'])(self.request.POST)
        else:
            data['questions'] = forms.formset_factory(QuestionForm, extra=self.kwargs['questions_count'])()
        return data

