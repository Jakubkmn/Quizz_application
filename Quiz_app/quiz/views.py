from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
        return redirect('quiz:quiz-update', quiz.pk)
    
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = '__all__'
    template_name = 'quiz/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().question_set.annotate(answer_count=Count('answer'))
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('quiz:quiz-update', kwargs={'pk': self.object.pk})

class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    success_url = reverse_lazy('quiz:quizes')

class QuestionCreateView(CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'quiz/question_add_form.html'

    def form_valid(self, form):
        form.instance.quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quiz:question-change', kwargs={'pk': self.object.quiz.pk, 'question_pk': self.object.pk})

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
    