from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        # if not name:
        #     raise ValueError("Name is required")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        user = self.create_user(email=email, name=name, password=password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", unique=True, max_length=225)
    name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



class Note(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=70, null=True, blank=True)
    body = models.CharField(max_length=1000,)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


  
