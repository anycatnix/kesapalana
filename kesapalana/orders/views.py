def orders_home(request):
	"""Landing page for /orders/ URL."""
	if request.user.is_authenticated:
		orders = Order.objects.filter(user=request.user).order_by('-created_at')
	else:
		orders = []
	return render(request, 'orders/orders_home.html', {'orders': orders})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem, Payment
from users.models import Address
from users.models import CustomUser
from products.models import Product
from django.core.mail import send_mail
from django.conf import settings

# Checkout view
@login_required
def checkout_view(request, username=None):
	# Only allow access to own checkout or staff
	if username and (username != request.user.username and not request.user.is_staff):
		messages.error(request, 'You do not have permission to checkout for this user.')
		return redirect('core:home')
	from cart.models import Cart, CartItem
	cart = Cart.objects.filter(user=request.user).first()
	if not cart or cart.items.count() == 0:
		messages.error(request, 'Your cart is empty.')
		return redirect('cart:cart_detail')
	if request.method == 'POST':
		shipping_address_id = request.POST.get('shipping_address')
		billing_address_id = request.POST.get('billing_address')
		shipping_address = Address.objects.get(id=shipping_address_id)
		billing_address = Address.objects.get(id=billing_address_id)
		order = Order.objects.create(
			user=request.user,
			shipping_address=shipping_address,
			billing_address=billing_address,
			status='pending',
		)
		total = 0
		for item in cart.items.all():
			OrderItem.objects.create(
				order=order,
				product=item.product,
				quantity=item.quantity,
				price=item.product.price
			)
			total += item.product.price * item.quantity
		order.total = total
		order.save()
		# Optionally clear the cart after order is placed
		cart.items.all().delete()
		# Send order confirmation email
		send_mail(
			'Order Confirmation',
			f'Thank you for your order #{order.id}!',
			settings.DEFAULT_FROM_EMAIL,
			[request.user.email],
		)
		return redirect('orders:payment', order_uuid=order.uuid)
	else:
		addresses = Address.objects.filter(user=request.user)
		print(f"[DEBUG] Addresses for user {request.user}: {list(addresses)}")
		return render(request, 'orders/checkout.html', {'addresses': addresses})

# Payment integration (simulate Razorpay/Stripe)
@login_required
def payment_view(request, order_uuid):
	order = get_object_or_404(Order, uuid=order_uuid, user=request.user)
	if request.method == 'POST':
		# Simulate payment success
		Payment.objects.create(
			order=order,
			payment_id='SIMULATED123',
			payment_method='razorpay',
			amount=order.total,
			status='success',
		)
		order.status = 'paid'
		order.save()
		messages.success(request, 'Payment successful!')
		return redirect('orders:order_status', order_uuid=order.uuid)
	return render(request, 'orders/payment.html', {'order': order})

# Order status tracking
@login_required
def order_status_view(request, order_uuid):
	order = get_object_or_404(Order, uuid=order_uuid, user=request.user)
	return render(request, 'orders/order_status.html', {'order': order})

# Refund logic
@login_required
def request_refund_view(request, order_uuid):
	order = get_object_or_404(Order, uuid=order_uuid, user=request.user)
	if request.method == 'POST':
		order.refund_requested = True
		order.save()
		messages.info(request, 'Refund requested. Our team will contact you soon.')
		# Optionally, send email to admin
		send_mail(
			f'Refund requested for Order #{order.id}',
			f'User {order.user.username} requested a refund.',
			settings.DEFAULT_FROM_EMAIL,
			[settings.DEFAULT_FROM_EMAIL],
		)
		return redirect('orders:order_status', order_uuid=order.uuid)
	return render(request, 'orders/request_refund.html', {'order': order})
