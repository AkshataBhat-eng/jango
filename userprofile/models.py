from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(blank=False, null=True) 
    address = models.CharField(max_length=500)
    mobile = models.IntegerField(default=9999999999)
