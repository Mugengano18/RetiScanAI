from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('result/<int:patient_id>/', resultDashboard, name="result"),
    path('form/', patientForm, name="form"),
    path('update_patient/<int:patient_id>/', update_patient, name="update_patient"),
]