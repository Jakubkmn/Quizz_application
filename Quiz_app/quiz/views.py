from django.shortcuts import render, redirect, get_object_or_404, reverse

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.db.models import Count
from django.db import transaction
from django.forms import inlineformset_factory

from .forms import QuestionForm, BaseAnswerInlineFormSet
from .models import Quiz, Question, Answer


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'quiz/login.html'
    fiels = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('quiz:quizes')

class RegisterPage(FormView):
    template_name = 'quiz/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('quiz:quizes')
        return super(RegisterPage, self).get(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('quiz:quizes')

class QuizList(LoginRequiredMixin, ListView):
    model = Quiz
    context_object_name = 'quizes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['quizes'] = context['quizes'].filter(name__startswith=search_input)

        context['search-input'] = search_input
        return context

class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'quiz/quiz.html'

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    fields = '__all__'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return redirect('quiz:quiz-update', quiz.pk)
    
class QuizUpdateView(LoginRequiredMixin, UpdateView):
    model = Quiz
    fields = '__all__'
    template_name = 'quiz/quiz_change_form.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().question_set.annotate(answer_count=Count('answer'))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('quiz:quiz-update', kwargs={'pk': self.object.pk})

class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    success_url = reverse_lazy('quiz:quizes')

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'quiz/question_add_form.html'

    def form_valid(self, form):
        form.instance.quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        messages.success(self.request, "You may now add answers to the question.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quiz:question-change', kwargs={'pk': self.object.quiz.pk, 'question_pk': self.object.pk})

@login_required
def question_change(request, pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    formset=BaseAnswerInlineFormSet,
    fields=('answer_text', 'correct'),
    min_num=2,
    validate_min=True,
    max_num=10,
    validate_max=True
    )
  
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('quiz:quiz-update', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    
    return render(request, 'quiz/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })
    