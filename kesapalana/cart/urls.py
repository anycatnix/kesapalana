# urls.py for cart app
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('<slug:username>/', views.cart_detail, name='cart_detail'),
    path('add/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<uuid:item_uuid>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<uuid:item_uuid>/', views.update_quantity, name='update_quantity'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
]
