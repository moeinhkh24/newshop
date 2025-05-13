from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .validators import valid_phone_number
from .managers import UserManager


class User(PermissionsMixin,AbstractBaseUser):
    phone_number = models.CharField(max_length=11,validators=[valid_phone_number],unique=True)
    username = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=125,)
    age = models.PositiveIntegerField(null=True,blank=True)#null=database,blank=website فیلد خالی
    is_active = models.BooleanField(default=True)
    is_admin =models.BooleanField(default=False)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email' , 'username','fullname']#واجبه که این سه تا باشه که تو ساخت سوپریوزر به ارور نخوریم

    objects = UserManager()
    
    def __str__(self):
        return f'{self.fullname}registerd by {self.phone_number}'
    
    @property
    def is_staff(self):
        return self.is_admin
    
