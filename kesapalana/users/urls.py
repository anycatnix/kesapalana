# urls.py for users app
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Legacy redirects for old URLs
    path('profile/', views.legacy_profile_redirect, name='legacy_profile'),
    path('addresses/', views.legacy_address_book_redirect, name='legacy_address_book'),
    path('address-book/', views.legacy_address_book_friendly_redirect, name='legacy_address_book_friendly'),
    path('orders/', views.legacy_order_history_redirect, name='legacy_order_history'),
    # New slug-based URLs
    path('profile/<slug:username>/', views.profile_view, name='profile'),
    path('addresses/<slug:username>/', views.address_book_view, name='address_book'),
    path('address-book/<slug:username>/', views.address_book_view, name='address_book_friendly'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('orders/<slug:username>/', views.order_history_view, name='order_history'),

    # Password reset
    path('password-reset/',
        views.PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'),
    path('password-reset/done/',
        views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/done/',
        views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),

    # Email confirmation (if using django-allauth or similar, add here)
    # JWT endpoints (add to main urls.py):
    # from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
