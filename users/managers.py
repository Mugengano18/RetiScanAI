from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullname, role, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, role=role, is_active=False, is_staff=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password):
        user = self.create_user(email, fullname, 'Admin', password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active=True
        user.save(using=self._db)
        return user