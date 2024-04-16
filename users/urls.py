from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', userRegister, name="register"),
    path('signin/', userLogin, name="login"),
]