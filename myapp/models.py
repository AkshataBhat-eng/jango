from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Akshata')
    address = models.CharField(max_length=255, default='address')
    mobile = models.IntegerField(default='9999999999')
    email = models.EmailField(blank=True, null=True) 