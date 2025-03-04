AUTHENTICATION_MANAGEMENT = ...

from django.db import models

""" Email and Password """
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('This Email Field Must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    # username = models.CharField(max_length=100, unique=False)
    first_name = models.CharField(max_length=100, unique=False)
    last_name = models.CharField(max_length=100, unique=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if this is a new user
        super().save(*args, **kwargs)
        if created:
            Customer.objects.create(user=self, email=self.email)


# For Registered Users to be Customers 
from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Customer

# Post_save signal automatically create a Customer object whenever a CustomUser is created.
@receiver(post_save, sender=CustomUser)
def create_customer_for_user(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance.email)


# Manage Company's Static Information 
class CompanyInfo(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo/')
    address = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    whatsapp_no = models.CharField(max_length=11)
    open_hours = models.CharField(max_length=100, blank=True, null=True)

    # social_handle  
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
        # blank = true - allows an admin to create record without passing value to it.. 
        # null = True - allow the database to store empty value, allows users...
    
    def __str__(self):
        return self.company_name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
