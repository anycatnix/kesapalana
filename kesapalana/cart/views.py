from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Coupon
from products.models import Product

def get_cart(request):
	if request.user.is_authenticated:
		cart, created = Cart.objects.get_or_create(user=request.user)
		return cart
	else:
		cart = request.session.get('cart', {})
		return cart

@login_required
def add_to_cart(request, product_slug):
	cart = get_cart(request)
	product = get_object_or_404(Product, slug=product_slug)
	item, created = CartItem.objects.get_or_create(cart=cart, product=product)
	if not created:
		item.quantity += 1
		item.save()
	messages.success(request, f'Added {product.name} to cart.')
	return redirect('cart:cart_detail', username=request.user.username)

@login_required
def remove_from_cart(request, item_uuid):
	cart = get_cart(request)
	item = get_object_or_404(CartItem, uuid=item_uuid, cart=cart)
	item.delete()
	messages.info(request, 'Item removed from cart.')
	return redirect('cart:cart_detail', username=request.user.username)

@login_required
def update_quantity(request, item_uuid):
	cart = get_cart(request)
	item = get_object_or_404(CartItem, uuid=item_uuid, cart=cart)
	if request.method == 'POST':
		quantity = int(request.POST.get('quantity', 1))
		item.quantity = quantity
		item.save()
		messages.success(request, 'Quantity updated.')
		username = request.POST.get('username', request.user.username)
	else:
		username = request.user.username
	return redirect('cart:cart_detail', username=username)

@login_required
def apply_coupon(request):
	cart = get_cart(request)
	if request.method == 'POST':
		code = request.POST.get('coupon')
		try:
			coupon = Coupon.objects.get(code=code, active=True)
			cart.coupon = coupon
			cart.save()
			messages.success(request, 'Coupon applied!')
		except Coupon.DoesNotExist:
			messages.error(request, 'Invalid coupon code.')
	return redirect('cart:cart_detail', username=request.user.username)

@login_required
def cart_detail(request, username=None):
	# Only allow access to own cart or staff
	if username and (username != request.user.username and not request.user.is_staff):
		messages.error(request, 'You do not have permission to view this cart.')
		return redirect('core:home')
	cart = get_cart(request)
	return render(request, 'cart/cart.html', {'cart': cart})
