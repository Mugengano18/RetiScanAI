from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', userRegister, name="register"),
    path('signin/', userLogin, name="login"),
    path('logout/', userLogout, name="logout"),
    path('verify-email-confirm/<uidb64>/<token>/',verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/',verify_email_complete, name='verify-email-complete'),
]