from django.urls import path
from . import views


app_name ='home'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('product/<int:pk>/',views.ProductDetailView.as_view(),name='product_detail'),
    path('comment/<int:pk>/',views.CommentCreateView.as_view(),name='comment_create')
]

