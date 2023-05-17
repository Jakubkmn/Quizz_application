from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
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