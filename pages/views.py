from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, PatientImage, ResultDescription
from django.db.models import Count
from django.contrib.auth import get_user_model
from .utils_model import load_and_preprocess_image, make_gradcam_heatmap, display_gradcam
from .utils.sms_utils import send_sms
import numpy as np
import tensorflow as tf
from .class_value import get_class
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
# Load the pre-trained model
model = tf.keras.models.load_model('C:\\Users\\Michel\\Documents\\Final_year_project\\diabetic_retinopathy_model_updated.h5')

# Define the last convolutional layer name
last_conv_layer_name = 'conv2d_5'  # Update this line

def home(request):
    return render(request, 'pages/index.html')
@login_required
def dashboard(request):
    users_per_page = 10
    search_patient = request.GET.get('search')
    if search_patient:
        patients = Patient.objects.filter(Q(full_name__icontains=search_patient) | Q(description__icontains=search_patient) | Q(predicted_class_name__icontains=search_patient) | Q(id__icontains=search_patient)).order_by("-id")
    else:
        patients = Patient.objects.order_by("-id")

    p = Paginator(patients, 10)
    page_number = request.GET.get('page',1)
    start_number = (int(page_number) - 1) * users_per_page + 1
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    no_dr_patients = Patient.objects.exclude(predicted_class_name='No_DR')

    class_counts = Patient.objects.values('predicted_class_name').annotate(count=Count('id'))
    class_counts_dict = {item['predicted_class_name']: item['count'] for item in class_counts}

    gender_counts = no_dr_patients.values('gender').annotate(count=Count('id'))
    gender_counts_dict = {item['gender']: item['count'] for item in gender_counts}

    context = {
        'patients': patients,
        'class_counts': class_counts_dict,
        'no_dr_patients': no_dr_patients,
        'gender_counts': gender_counts_dict,
        'page_obj': page_obj,
        "start_number": start_number,
    }

    return render(request, 'pages/dashboard.html', context)

@login_required
def resultDashboard(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    stage_note = ResultDescription.objects.get(name= patient.predicted_class_name)
    context = {
        'patient': patient,
        'stage_note':stage_note,
    }
    return render(request, "pages/resultDashboard.html",context)
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
        
        patient.save()
         # Get the URL and path of the saved image
        image_url = patient.eye_image.url
        image_path = patient.eye_image.path

        # Load and preprocess the image
        X_instance = load_and_preprocess_image(image_path)

        # Get the model's prediction
        preds = model.predict(X_instance)
        predicted_class = np.argmax(preds[0])
        formatted_probabilities = ['{:.2f}'.format(prob) for prob in preds[0]]
        class_name = get_class(predicted_class)

        # Generate the Grad-CAM heatmap
        heatmap = make_gradcam_heatmap(X_instance, model, last_conv_layer_name,predicted_class)
       


        # Display the original image and the Grad-CAM heatmap
        original_image, gradcam_image, quadrant_image = display_gradcam(image_path, heatmap)
        patient.predicted_class = predicted_class
        patient.gradcam_image = gradcam_image
        patient.predicted_class_name=class_name
        patient.probability=formatted_probabilities
        patient.quadrants_image = quadrant_image


        patient.save()
        return redirect('result',patient_id=patient.id)
    return render(request, 'pages/form.html')

def update_patient(request, patient_id):
    if request.method =="POST":
        patient = get_object_or_404(Patient, id=patient_id)
        description = request.POST.get('description')
        patient.description = description
        patient.is_confirm = True
        send_sms(patient)
        patient.save()	
        return redirect('result',patient_id=patient.id)
    return redirect('result',patient_id=patient.id)


def check(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES.get('image')
        # Save the image to the database
        patient_image = PatientImage(image=image_file)
        patient_image.save()
        # Get the URL and path of the saved image
        image_url = patient_image.image.url
        image_path = patient_image.image.path
        # Load and preprocess the image
        X_instance = load_and_preprocess_image(image_path)
        # Get the model's prediction
        preds = model.predict(X_instance)
        predicted_class = np.argmax(preds[0])
        # Generate the Grad-CAM heatmap
        heatmap = make_gradcam_heatmap(X_instance, model, last_conv_layer_name, predicted_class)
        # Display the original image and the Grad-CAM heatmap
        original_image, gradcam_image = display_gradcam(image_path, heatmap)
        context = {
            'predicted_class': predicted_class,
            'original_image': original_image,
            'gradcam_image': gradcam_image,
            'uploaded_image_url': image_url
        }
        return render(request, 'pages/check.html', context)
    return render(request, 'pages/check.html')

def gender_counts_json(request):
    no_dr_patients = Patient.objects.exclude(predicted_class_name='No_DR')
    gender_counts = no_dr_patients.values('gender').annotate(count=Count('id'))
    gender_counts_dict = {item['gender']: item['count'] for item in gender_counts}
    return JsonResponse(gender_counts_dict)

def admin_dashboard(request):
    users_per_page = 10
    search_user = request.GET.get('search_user')
    if search_user:
        users = get_user_model().objects.filter(Q(fullname__icontains=search_user) | Q(email__icontains=search_user) | Q(id__icontains=search_user)).exclude(is_deleted=True).order_by("-id")
    else:
        users = get_user_model().objects.order_by("-id").exclude(is_deleted=True)
    p = Paginator(users, 10)
    page_number = request.GET.get('page',1)
    start_number = (int(page_number) - 1) * users_per_page + 1
    
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {
            "page_obj":page_obj,
            "start_number": start_number,
        }

    return render(request, 'pages/adminDashboard.html', context)


def delete_user(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
        user.is_deleted = True
        user.save()
        messages.sucess(request, "The user is deleted")
    except:
        messages.error(request, "The user not found")
    return redirect('admin_dashboard') 

