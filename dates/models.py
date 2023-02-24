from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    


class ImageHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_number = models.IntegerField()
    is_accepted = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)