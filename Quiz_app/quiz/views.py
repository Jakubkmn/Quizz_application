from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .forms import SignUpForm, QuizForm, QuestionForm, AnswerForm
from .models import Quiz, Question

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
            new_quiz = form.save()
            # name = form.cleaned_data['name']
            # topic = form.cleaned_data['topic']
            # num_of_questions = form.cleaned_data['number_of_questions']

            # new_quiz = Quiz(name=name, topic=topic, number_of_questions=num_of_questions)
            # new_quiz.save()

            # return redirect('quiz:create_question', quiz_id=new_quiz.id)
            return redirect('quiz:create_question', quiz_id=new_quiz.id)
    else:
        form = QuizForm()
        context = {
            'form': form
        }
            
    return render(request, 'quiz/create_quiz.html', context)

def create_question(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:home')
            # question_text = form.cleaned_data['question_text']

            # choice1 = form.cleaned_data["choice1_text"]
            # choice1_correctness = form.cleaned_data["choice1_correctness"]

            # choice2 = form.cleaned_data["choice2_text"]
            # choice2_correctness = form.cleaned_data["choice2_correctness"]

            # choice3 = form.cleaned_data["choice3_text"]
            # choice3_correctness = form.cleaned_data["choice3_correctness"]

            # choice4 = form.cleaned_data["choice4_text"]
            # choice4_correctness = form.cleaned_data["choice4_correctness"]

            # question = Question(question_text=question_text, quiz=quiz, question_num=question_id)
            # question.save()

            # question.choice_set.create(choice_text=choice1, correct=choice1_correctness)
            # question.choice_set.create(choice_text=choice2, correct=choice2_correctness)
            # question.choice_set.create(choice_text=choice3, correct=choice3_correctness)
            # question.choice_set.create(choice_text=choice4, correct=choice4_correctness)

            # if question_id == quiz.number_of_questions:
            #     return redirect('quiz:home')
            # else:
            #     next_question_id = question_id + 1
            #     return redirect('quiz:create_question', quiz_id=quiz_id)
    else:
        form = QuestionForm()
        

    context = {
        'form': form
        # 'question_num': question_id
    }

    return render(request, 'quiz/create_question.html', context)

