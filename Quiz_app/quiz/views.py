from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
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
        return render(request, 'quiz/home.html', {})

def logout_user(request):
    pass