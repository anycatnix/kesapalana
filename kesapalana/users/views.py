
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, UserProfile, Address, Wishlist
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.decorators.http import require_POST
from orders.models import Order
# Password reset views
from django.contrib.auth.views import (
	PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

# Legacy redirects for old URLs
@login_required
def legacy_profile_redirect(request):
	return redirect('users:profile', username=request.user.username)

@login_required
def legacy_address_book_redirect(request):
	return redirect('users:address_book', username=request.user.username)

@login_required
def legacy_address_book_friendly_redirect(request):
	return redirect('users:address_book_friendly', username=request.user.username)

@login_required
def legacy_order_history_redirect(request):
	return redirect('users:order_history', username=request.user.username)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, UserProfile, Address, Wishlist
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.decorators.http import require_POST
from orders.models import Order

# Password reset views
from django.contrib.auth.views import (
	PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

def register_view(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			UserProfile.objects.create(user=user)
			login(request, user)
			return redirect('users:profile', username=user.username)
	else:
		form = CustomUserCreationForm()
	return render(request, 'users/register.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('users:profile', username=user.username)
	else:
		form = CustomAuthenticationForm()
	return render(request, 'users/login.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('users:login')

from .forms import UserProfileForm
@login_required
def profile_view(request, username=None):
	if username and (username != request.user.username and not request.user.is_staff):
		messages.error(request, 'You do not have permission to view this profile.')
		return redirect('core:home')
	try:
		profile = request.user.profile
	except UserProfile.DoesNotExist:
		profile = UserProfile.objects.create(user=request.user)
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile updated successfully!')
			return redirect('users:profile', username=request.user.username)
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'users/profile.html', {'profile': profile, 'form': form})

@login_required
def address_book_view(request, username=None):
	if username and (username != request.user.username and not request.user.is_staff):
		messages.error(request, 'You do not have permission to view this address book.')
		return redirect('core:home')
	from .forms import AddressForm
	addresses = request.user.addresses.all()
	next_url = request.GET.get('next')
	if request.method == 'POST':
		form = AddressForm(request.POST)
		if form.is_valid():
			address = form.save(commit=False)
			address.user = request.user
			address.save()
			messages.success(request, 'Address added successfully!')
			if next_url:
				return redirect(next_url)
			return redirect('users:address_book_friendly')
	else:
		form = AddressForm()
	return render(request, 'users/address_book.html', {'addresses': addresses, 'form': form, 'next': next_url})

@login_required
def wishlist_view(request):
	wishlist, created = Wishlist.objects.get_or_create(user=request.user)
	return render(request, 'users/wishlist.html', {'wishlist': wishlist})

@login_required
def order_history_view(request, username=None):
	if username and (username != request.user.username and not request.user.is_staff):
		messages.error(request, 'You do not have permission to view this order history.')
		return redirect('core:home')
	orders = Order.objects.filter(user=request.user)
	return render(request, 'users/order_history.html', {'orders': orders})
