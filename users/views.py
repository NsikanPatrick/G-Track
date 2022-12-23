from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check for privilege so you know the panel to redirect the user to
            # This works directly with the django's user model, which means, it
            # checks for the user from the django admin
            login(request, user)
            return redirect('index')
        else:
            # {"message": "Access denied, your credentials are invalid"}
            messages.success(request, "Access denied, your login credentials are invalid")
            return redirect('login')
    return render(request, 'authentication/login.html', {})
    

def logout_view(request):
    logout(request)
    # return render(request, "authentication/login.html", {"message": "logged out"})
    return redirect('login')