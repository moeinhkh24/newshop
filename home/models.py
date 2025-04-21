from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from . import manager

class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True , blank=True) #aws
    text = models.TextField()
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.title} and {self.price}'
    

    def get_absolute_url(self):
        return reverse("home:product_detail", kwargs={"pk": self.pk})
    


class Comment(models.Model):
    STARS_CHOICES = [
        ('1','⭐'),
        ('2','⭐⭐'),
        ('3','⭐⭐⭐'),
        ('4','⭐⭐⭐⭐'),
        ('5','⭐⭐⭐⭐⭐')
    ]

    product = models.ForeignKey(Product,on_delete =models.CASCADE,related_name='comments')
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    text =models.TextField()
    stars =models.CharField(max_length=128,choices=STARS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    #Managers
    objects = models.Manager()
    cm_manager = manager.ActiveCommentManager()

    def __str__(self):
        return f'{self.author.username} Write a comment about {'self.product'}:{'self.text'}'
    def get_absolute_url(self):
        return reverse("home:product", kwargs={"pk": self.pk})
    
