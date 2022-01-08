import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from cryptography.fernet import Fernet
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


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
            message = render_to_string('emails/acc_active_email.html', {
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
    if user_id == str(request.user.id):
        user = CustomUser.objects.get(id=user_id)
        return render(request, 'users/dashboard.html', {'user': user})
    else:
        msg = "currently loged user: " + str(request.user.id) + "passed id from login: " + user_id
        return HttpResponse(msg)

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

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    subject = "Password Reset Requested"
                    email_template_name = "emails/password_reset.html"
                    c = {
                    "email":user.email,
                    'domain': current_site.domain,
                    'site_name': 'Dail-in',
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    message = render_to_string(email_template_name, c)
                    email = EmailMessage( subject, message, to=[user.email])
                    email.send()
                    return redirect ('users:password_reset_done')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="passwords/password_reset.html", context={"password_reset_form":password_reset_form})

def PasswordResetConfirmView(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        update_session_auth_hash(request, user)
        msg = "Thank you "+ user.first_name +" Password Succesfully updated!"
        messages.success(request, msg)
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = True
                user.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('users:login')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = SetPasswordForm(request.user)
        return render(request, 'passwords/password_reset_confirm.html', { 'form': form })
    else:
        return HttpResponse('Activation link is invalid!')
