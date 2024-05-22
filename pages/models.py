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
    eye_image = models.ImageField(upload_to='eye_images/')
    description = models.TextField(null=True)
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
