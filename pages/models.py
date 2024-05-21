from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    ]

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    eye_image = models.ImageField(upload_to='eye_images/')

    def __str__(self):
        return self.full_name
