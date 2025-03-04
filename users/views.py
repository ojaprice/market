from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, CustomPasswordResetForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView

# to add sending of mail 
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


User = get_user_model()

def signup_page(request):
    """
    User registration
    """
    if request.method == 'POST':
        # form
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.is_active = False  # User not active - 0 
            user.save()
            
            # Generate email verification token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            verification_link = f"http://{domain}/activate/{uid}/{token}/"

            # Send email
            subject = "Verify Your Email"
            html_message = render_to_string('emails/email_verification.html', {
                'user': user,
                'verification_link': verification_link
            })

            email = EmailMessage(
                subject=subject,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
                body=html_message
            )
            email.content_subtype = "html"
            email.send()     

            messages.success(request, "A verification email has been sent. Please check your inbox.")
            return redirect('login')        
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def activate_account(request, uidb64, token):
    """
    Function activates account when URL in email is clicked
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been successfully activated! You can now log in.")
        return redirect('login')  
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect('register')
    

class CustomLoginView(LoginView):
    """
    Class handles login
    """
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('index')  

def logout_view(request):
    logout(request)
    return redirect("index")


from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy("Password Reset done")
    