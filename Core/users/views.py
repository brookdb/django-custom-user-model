import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cryptography.fernet import Fernet
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False

            #encrypt user id using Fernet and send to email template alongside the userID
            current_site = get_current_site(request)
            id = user.id.hex
            key = Fernet.generate_key()
            user.token = key.decode('utf-8')
            #save user data to database
            user.save()
            #encrypt user ID
            fernet = Fernet(key)
            encID = fernet.encrypt(id.encode())

            #start constructing activation email
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'ID': id,
                'encID': encID.decode('utf-8'),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage( mail_subject, message, to=[to_email])
            email.send()
            messages.info(request, 'Please confirm your email address to complete the registration')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('users:dashboard', user_id=user.id)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')

@login_required(login_url="/users/login/")
def dashboard_view(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'users/dashboard.html', {'user': user})

def activate(request, ID, encID):
    try:
        user_id = str(uuid.UUID(ID))
        user = CustomUser.objects.get(id=user_id)
        fernet = Fernet(user.token)
        encID_bytes = bytes(encID, 'utf-8')
        decID = str(uuid.UUID(fernet.decrypt(encID_bytes).decode()))
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as err:
        user = 'None'
        decID = err

    finally:
        if user != 'None' and str(user_id) == decID:
            user.is_active = True
            user.save()
            #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
            msg = '<h3>User Found!</h3><p>email: '+user.email+'</p><p>decID: '+ decID +'</p><p>user_id: '+str(user_id)+'</p>'
            return HttpResponse(msg)
        else:
            msg = '<h3>Activation link is invalid!</h3>'+'<p>user: '+ str(user) +'</p>'+'<p>ID: '+ str(user_id) +'</p>'+'<p>encID: '+ encID +'</p>'+'<p>decID: '+ decID +'</p><br><br>'
            account = CustomUser.objects.get(id=str(user_id))
            msg = msg + account.email
            return HttpResponse(msg)
