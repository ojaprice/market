from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordResetForm, # to custom password requirement
)
from django.contrib.auth import get_user_model


# import custom user 
User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    # username = forms.CharField(max_length=40)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'password1', 'password2']
        

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'mb-2', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': '', 'placeholder': 'Password'}))

    
# PasswordReset   
class CustomPasswordResetForm(PasswordResetForm):
    """
    To validate if email to be submitted by the user is in the database.
    """
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not associated with any account")
        return email
    
