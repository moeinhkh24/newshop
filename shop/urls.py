from django.urls import path
from . import views


app_name='shop'


urlpatterns = [
    path('',views.CartView.as_view(),name='test'),
    path('cart/add/<int:product_id>',views.CartAddView.as_view(),name='cart_add'),
    path('cart/remove/<int:product_id>'.views.CartRemoveView.as_view(),name='cart_remove'),
    path('cart/clear/',views.CartClearView.as_view(),name='cart_clear'),
]
