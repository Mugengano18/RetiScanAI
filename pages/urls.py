from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('dashboard/', dashboard, name="dashboard"),
    path('result/<int:patient_id>/', resultDashboard, name="result"),
    path('form/', patientForm, name="form"),
    path('update_patient/<int:patient_id>/', update_patient, name="update_patient"),
    path('api/gender-counts/', gender_counts_json, name='gender_counts_json'),
    path('adminDashboard/',admin_dashboard, name="admin_dashboard"),
    path('delete_user/<int:user_id>/',delete_user, name="delete_user"),
]