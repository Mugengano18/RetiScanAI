from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient

def home(request):
    return render(request, 'pages/index.html')
@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')

def resultDashboard(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, "pages/resultDashboard.html",{'patient': patient})

def patientForm(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        birth_date = request.POST.get('birth_date')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        eye_image = request.FILES.get('eye_image')

        patient = Patient(
            full_name=full_name,
            birth_date=birth_date,
            phone_number=phone_number,
            gender=gender,
            eye_image=eye_image
        )
        patient.save()

        return redirect('result',patient_id=patient.id)
    return render(request, 'pages/form.html')
