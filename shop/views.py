from django.shortcuts import render
from django.views import View
from .cart import Cart
from .forms import AddToCartForm
from home.models import Product


def CartView(View):
    def get(self,request):
        cart = Cart(request)
        for item in cart:
            item['quantity_update_form'] = AddToCartForm(initial={
                'quantity':item['quantity'],
                'inplace':True  
            })
        return render(request,'shop/cart.html',{'cart':cart})

def CartAddView(View):
    pass

def CartRemoveView(View):
    pass

def CartClearView(View):
    pass
