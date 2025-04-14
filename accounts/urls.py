from django.urls import path
from.import views

app_name = 'accounts'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(), name='user_register'),
    path('verifycode/',views.VerifyOtpCodeView.as_view(),name='verifycode')
]
