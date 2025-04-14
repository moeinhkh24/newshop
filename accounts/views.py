import random
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import get_user_model
from .forms import OtpForm,UserRegisterForm,UserLoginForm
from .models import OtpCode,User


class UserRegisterView(View):
    form_class = UserRegisterForm
    temp = 'accounts/register.html'


    def get(self,request):
        form = self.form_class()
        return render(request,self.temp,{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            random_otp = random.randint(1000,9999)
            OtpCode.objects.create(phone =cd['phone_number'],code = random_otp)
            request.session['user_info'] = {
                'phone_number':cd['phone_number'],
                'email':cd['email'],
                'username':cd['username'],
                'fullname':cd['fullname'],
                'password':cd['password'],
            }
            return redirect('accounts:verifycode')
        return render(request,self.temp,{'form':form})        

class VerifyOtpCodeView(View):
    form_class = OtpForm
    temp ='accounts/verifycode.html'


    def get(self,request):
        form = self.form_class()
        print(dict(request.session))
        return render(request,self.temp,{'form':form})
    

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = request.session['user_info']
        otpcode = OtpCode.objects.get(phone =user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if str(cd['code']) == str(otpcode):
                User.objects.create_user(
                    phone_number = user_session['phone_number'],
                    username = user_session['username'],
                    email = user_session['email'],
                    fullname = user_session['fullname'],
                    password =user_session['password']
                )
                return redirect('home:home')
            return render(request,self.temp,{'form':form})
        return render(request,self.temp,{'form':form})
    


#hjfdgvrtfgvbuujt #پرسپولیس