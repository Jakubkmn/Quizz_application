from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .forms import SignUpForm, QuizForm, QuestionForm, AnswerForm
from .models import Quiz

# Create your views here.


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('quiz:home')
        else:
            messages.success(request, "There was an error logging in. Please try again")
            return redirect('quiz:home')
    else:
        return render(request, 'quiz/home.html', {'user': request.user})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('quiz:home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('quiz:home')
    else:
        form = SignUpForm()
        return render(request, 'quiz/register.html', {'form':form})
    return render(request, 'quiz/register.html', {'form':form})

def quiz_results(request):
    return render(request, 'quiz/quiz_results.html', {})

def play(request):
    quizzes = Quiz.objects.all()

    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')
        return redirect('quiz:take_quiz', quiz_id=quiz_id)
    return render(request, 'quiz/play.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    questions = quiz.question_set.all()
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions))

    if request.method == 'POST':
        formset = AnswerFormSet(request.POST, prefix='answer')
        if formset.is_valid():
            for i, form in enumerate(formset):
                answer = form.save(commit=False)
                answer.question = questions[i]
                answer.save()

            return redirect('quiz:quiz_results', quiz_id=quiz.id)

    else:
        formset = AnswerFormSet(prefix='answer')

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions, 'formset': formset})


def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            topic = form.cleaned_data['topic']
            num_of_questions = form.cleaned_data['number_of_questions']
            time = form.cleaned_data['time']

            new_quiz = Quiz(name=name, topic=topic, number_of_questions=num_of_questions, time=time)
            new_quiz.save()

            return redirect('quiz:create_question', quiz_id=new_quiz.id)
            # return render(request, 'quiz/question_creator.html', {})
    else:
        form = QuizForm()
        context = {
            'form': form
        }
            
    return render(request, 'quiz/create.html', context)

def create_question(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if request.method == 'POST':
        num_questions = int(request.POST.get('number_of_questions', 0))
        formset = formset_factory(QuestionForm, extra=num_questions)
        formset = formset(request.POST)
        if formset.is_valid():
            for form in formset:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()

            return redirect('quiz:home')

    else:
        num_questions = quiz.number_of_questions
        formset = formset_factory(QuestionForm, extra=1)

    return render(request, 'quiz/question_creator.html', {'formset': formset, 'quiz': quiz})

