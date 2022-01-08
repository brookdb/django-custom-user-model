from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Password confirmation',
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
        }

class CustomPasswordResetForm(PasswordResetForm):

    class Meta:
        model = CustomUser
        fields = ('email',)
        labels = {
            'email': 'Email',
        }
