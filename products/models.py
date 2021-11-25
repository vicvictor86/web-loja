from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Products(models.Model):
    product_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    product_resume = models.CharField(max_length=500)
    comment1 = models.CharField(max_length=500)
    comment2 = models.CharField(max_length=500)
    product_informations = models.CharField(max_length=500)
    reasons_to_buy = models.CharField(max_length=500)
    date_product = models.DateTimeField(default=datetime.now, blank=True)
    photo = models.ImageField(upload_to='fotos/%d/%m%Y', blank = True)
    public = models.BooleanField(default=False)
    def __str__(self):
        return self.name