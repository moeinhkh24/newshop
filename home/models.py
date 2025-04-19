from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField() #aws
    text = models.TextField()
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    