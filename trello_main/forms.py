from django import forms  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import CustomUser as User

class SignupForm(UserCreationForm):  
    email = forms.EmailField(max_length=200, help_text='Required')  

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
       return self.cleaned_data

    class Meta:  
        model = User  
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )  

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')
    