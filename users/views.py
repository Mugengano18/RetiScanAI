from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from users.utils.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages

def userRegister(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, 'That email is already in use')
                return redirect('register')
            else:
                user = get_user_model().objects.create_user(email=email, password=password, role=role, fullname=fullname)
                user.save()
                current_site = get_current_site(request)
                subject = "Verify Email"
                message = render_to_string('users/verify_email_message.html', {
                'request': request,
                'user': fullname,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                })
                email_message = EmailMessage(
                subject, message, to=[email]
                )
                email_message.content_subtype = 'html'
                email_message.send()
                messages.success(request, 'You are now registered and verify your Email')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'users/signup.html')

def userLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            print("login     ", user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'users/signin.html')
    
def userLogout(request):
    logout(request)
    return redirect("home")





def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified.')
        return redirect('verify-email-complete')   
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'users/verify_email_confirm.html')

def verify_email_complete(request):
    return render(request, 'users/verify_email_complete.html')