from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from .utils.sms_utils import send_sms

def home(request):
    return render(request, 'pages/index.html')
@login_required
def dashboard(request):
    patients = Patient.objects.all()
    return render(request, 'pages/dashboard.html', {'patients': patients})
@login_required
def resultDashboard(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, "pages/resultDashboard.html",{'patient': patient})
@login_required
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
        print("send sms response status:", send_sms(patient))
        patient.save()

        return redirect('result',patient_id=patient.id)
    return render(request, 'pages/form.html')

def update_patient(request, patient_id):
    if request.method =="POST":
        patient = get_object_or_404(Patient, id=patient_id)
        description = request.POST.get('description')
        patient.description = description
        patient.is_confirm = True
        patient.save()	
        return redirect('result',patient_id=patient.id)
    return redirect('result',patient_id=patient.id)

