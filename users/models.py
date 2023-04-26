from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User

# Create your models here.

class UserProfile(models.Model):
    """ User profile """
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='profile_images', blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    def get_name(self):
        if self.user.name:
            return self.user.name
        elif self.user.username:
            return self.user.username    
        else:
            return f"User{self.user.id}"

    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return '/static/img/default_profile.png'

# class Progress(models.Model):
#     user = models.OneToOneField('User', on_delete=models.CASCADE)
#     progress_percent = models.IntegerField(default=0)
#     last_visit_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.name} - {self.progress_percent}%"

class UserManager(BaseUserManager):
    """ Manager for users """

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create Superuser in the System
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()