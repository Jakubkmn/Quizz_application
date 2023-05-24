from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Quiz
from .forms import QuizForm
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

def play(request):
    return render(request, 'quiz/play.html', {})

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

            return render(request, 'quiz/question_creator.html', {})
    else:
        form = QuizForm()
        context = {
            'form': form
        }
            
    return render(request, 'quiz/create.html', context)
