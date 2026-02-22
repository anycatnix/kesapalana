# urls.py for products app
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_list, name='search'),
    path('category/<slug:category_slug>/', views.product_list, name='category_filter'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/review/', views.add_review, name='add_review'),
]
