from django.contrib.auth.models import BaseUserManager
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, fullname, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password):
        user = self.create_user(email, fullname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user