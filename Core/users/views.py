from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CustomUserCreationForm
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            return HttpResponse('<h1>Form is Valid</h1>')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    return HttpResponse('<h1>login  view</h1>')

def logout_view(request):
    return HttpResponse('<h1>Log out view</h1>')
