import random
from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.http import HttpResponseNotAllowed
from .models import User
from .forms import OtpForm, UserRegisterForm, UserLoginForm
from utils.redis_utils import redis_manager


class UserRegisterView(View):
    form_class = UserRegisterForm
    temp = 'accounts/register.html'


    def get(self, request):
        form = self.form_class()
        return render(request, self.temp, {'form':form})        
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            otp_code = redis_manager.generate_otp(phone_number=cd['phone_number'])
            print(f'{otp_code} for phonenumber')
            request.session['user_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'username': cd['username'],
                'fullname': cd['fullname'],
                'password': cd['password']
            }
            return redirect('accounts:verifycode')
        return render(request , self.temp, {'form':form})
    
class VerifyOtpCodeView(View):
    form_class = OtpForm
    temp = 'accounts/verifycode.html'
    
    
    def get(self, request):
        form = self.form_class()
        print(dict(request.session))
        return render(request, self.temp, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_info']
        if form.is_valid():
            cd = form.cleaned_data
            if redis_manager.validate_otp(user_session['phone_number'], str(cd['code'])):
                User.usermanager.create_user(
                    phone_number=user_session['phone_number'],
                    username=user_session['username'],
                    email=user_session['email'],
                    fullname=user_session['fullname'],
                    password=user_session['password']
                )
                return redirect('home:home')
            else:
                form.add_error('code', 'Invalid input')
        return render(request, self.temp, {'form':form})

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('home:home')
            return render(request, self.template_name, {'form':form})
        return render(request, self.template_name, {'form':form})
    
    
class UserLogoutView(View):
    
    def get(self, request):
        response = render(request, '405.html')
        return HttpResponseNotAllowed(['POST'], response)
    
    def post(self, request):
        logout(request)
        return redirect('home:home')