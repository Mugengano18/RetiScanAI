from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=9, choices=GENDER_CHOICES)
    predicted_class = models.IntegerField(null=True, blank=True)
    predicted_class_name = models.CharField(max_length=30, null=True, blank=True)
    probability = models.TextField(null=True, blank=True)
    eye_image = models.ImageField(upload_to='eye_images/')
    gradcam_image = models.TextField(null=True, blank=True)
    quadrants_image = models.TextField(null=True, blank=True)
    description = models.TextField(null=True)

    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    
    
class ResultDescription(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    characteristic = models.TextField(null=True, blank=True)
    quadrant_analysis=models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
