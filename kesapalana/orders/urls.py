# urls.py for orders app
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.orders_home, name='orders_home'),
    path('checkout/<slug:username>/', views.checkout_view, name='checkout'),
    path('payment/<uuid:order_uuid>/', views.payment_view, name='payment'),
    path('status/<uuid:order_uuid>/', views.order_status_view, name='order_status'),
    path('refund/<uuid:order_uuid>/', views.request_refund_view, name='request_refund'),
]
