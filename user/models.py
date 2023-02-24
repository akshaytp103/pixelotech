

# Create your models here.
from django.db import models

class User(models.Model):
    mobile = models.CharField(max_length=10)
    name = models.CharField(max_length=50, null=True, blank=True)
    is_verified = models.BooleanField(default=False) 