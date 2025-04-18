from django.urls import path
from . import views
from django.views import generic
app_name ='home'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('detail/',generic.TemplateView.as_view(template_name='home/product-details.html'),name='detail')
]

