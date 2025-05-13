from typing import Any
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Product, Comment
from .forms import CommentForm
from shop.forms import AddToCartForm
from django.http import HttpResponse
from utils.redis_utils import redis_manager



class HomeView(generic.ListView):
    queryset = Product.objects.filter(active=True)
    template_name = 'home/index.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        session_id = request.session.session_key or request.META.get('REMOTE_ADDR')
        redis_manager.track_daily_visit(session_id)
        return super().get(request, *args, **kwargs)
        
class ProductDetailView(generic.DetailView):
    queryset = Product.objects.prefetch_related(Prefetch
                                                ('comments',
                                                 queryset=Comment.cm_manager.select_related(
                                                     'author')
                                                 )
                                                )
    template_name = 'home/product-details.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['add_cart_form'] = AddToCartForm()
        return context
    
class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'home/product-details.html'


    def get_success_url(self) -> str:
        return reverse('home:product_detail', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        pk = int(self.kwargs['pk'])
        product = get_object_or_404(Product, pk=pk)
        obj.product = product
        return super().form_valid(form)
        