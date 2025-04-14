from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self,phone_number,username,email,fullname,password,*args, **kwargs):

        if not phone_number:
            raise ValueError('User has to have PhoneNumber')
        
        if not username:
            raise ValueError("Users Has to have Username")
        
        if not email:
            raise ValueError("Users has to have Email")
        if not fullname:
            raise ValueError("You Have to enter Fullname")
        
        user = self.model(phone_number=phone_number,username=username,email=self.normalize_email(email),fullname=fullname)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self,phone_number,username,email,fullname,password,*args, **kwargs):

        user = self.create_user(phone_number,username,email,fullname,password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user