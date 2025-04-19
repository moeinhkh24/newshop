from django.shortcuts import render
from django.views import generic
from .models import Product
class HomeView(generic.ListView):
    queryset = Product.objects.filter(active =True)
    template_name = 'home/index.html'
    context_object_name = 'products'
    paginate_by = 10