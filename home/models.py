from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from . import manager

class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    text = models.TextField()
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.title} and {self.price}'
    
    def get_absolute_url(self):
        return reverse("home:product_detail", kwargs={"pk": self.pk})
    

class Comment(models.Model):
    STARS_CHOICES = [
        ('1', 'verybad'),
        ('2', 'bad'),
        ('3', 'normal'),
        ('4', 'good'),
        ('5', 'perfect')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    stars = models.CharField(max_length=1, choices=STARS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)  # اصلاح تایپو
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()
    cm_manager = manager.ActiveCommentManager()
    
    def __str__(self):
        return f'{self.author.username} wrote a comment about {self.product}: {self.text}'
    
    def get_absolute_url(self):
        return reverse("home:product", kwargs={"pk": self.product.pk})  # اصلاح لینک

