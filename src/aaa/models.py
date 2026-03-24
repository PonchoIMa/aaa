from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Role(models.Model):
    name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    email       = models.EmailField(unique = True)
    first_name  = models.CharField(max_length = 150)
    last_name   = models.CharField(max_length = 150)
    role        = models.ForeignKey(Role, on_delete = models.SET_NULL, null = True)
    is_active   = models.BooleanField(default = True) # Soft delete flag

    USERNAME_FIELD = 'email'

class BusinessElement(models.Model):
    # This can eventually amplified 
    # Different ID and path since, path can be altered, and for better handling
    numb = models.IntegerField(unique = True)
    path = models.CharField(max_length = 100, unique = True)

class AccessRoleRule(models.Model):
    role    = models.ForeignKey(Role, on_delete = models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete = models.CASCADE)
    
    # Permissions 'crud' which the program will read to grant permissions
    permissions = models.CharField(max_length = 4, default = 'r')
