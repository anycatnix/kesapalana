from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Address, Wishlist

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	list_display = ('username', 'email', 'is_staff', 'is_active')
	search_fields = ('username', 'email')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'phone', 'date_of_birth')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = ('user', 'full_name', 'city', 'country', 'is_default')
	list_filter = ('country', 'is_default')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
	list_display = ('user',)
