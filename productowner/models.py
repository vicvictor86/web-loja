from django.db import models
from django.db.models.base import Model
from django.conf import settings

# Create your models here.
class Client(models.Model):
    client = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fund = models.DecimalField(decimal_places=2, max_digits=9)
    
    def __str__(self):
        return self.client.username + "_clients"
