# urls.py for core app
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('science/', views.science_page, name='science'),
    path('about/', views.about_page, name='about'),
    path('testimonials/', views.testimonials_page, name='testimonials'),
    path('contact/', views.contact_page, name='contact'),
    path('newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('success-stories/', views.success_stories_page, name='success_stories'),
    path('ingredients/', views.ingredients_page, name='ingredients'),
]
