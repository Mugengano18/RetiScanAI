from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, PatientImage

from .utils_model import load_and_preprocess_image, make_gradcam_heatmap, display_gradcam
from .utils.sms_utils import send_sms
import numpy as np
import tensorflow as tf
from .class_value import get_class
# Load the pre-trained model
model = tf.keras.models.load_model('C:\\Users\\Michel\\Documents\\Final_year_project\\diabetic_retinopathy_model_updated.h5')

# Define the last convolutional layer name
last_conv_layer_name = 'conv2d_5'  # Update this line

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
        original_image, gradcam_image = display_gradcam(image_path, heatmap)
        patient.predicted_class = predicted_class
        patient.gradcam_image = gradcam_image
        patient.predicted_class_name=class_name
        patient.probability=formatted_probabilities

        patient.save()

        # context = {
        # 'predicted_class': predicted_class,
        # 'original_image': original_image,
        # 'gradcam_image': gradcam_image,
        # 'uploaded_image_url': image_url
        # }

        # return redirect('result',patient_id=patient.id)
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

        print("++++++++++++++++++++++++ image_url:", image_url)
        print("=================================image_path", image_path)
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

