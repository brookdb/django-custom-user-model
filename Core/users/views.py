from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CustomUserCreationForm
from .models import CustomUser
# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            return redirect('users:dashboard', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    return HttpResponse('<h1>login  view</h1>')

def logout_view(request):
    return HttpResponse('<h1>Log out view</h1>')

def dashboard_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    html_string='<h1>Dashboard view</h1><br><p>'+str(user.id) +'</p><p>Welcome '+ str(user.email)
    return HttpResponse(html_string)
