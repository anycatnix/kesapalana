from django.db import models

from django.conf import settings
import uuid
from users.models import Address

class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_addresses')
	full_name = models.CharField(max_length=100)
	address_line1 = models.CharField(max_length=255)
	address_line2 = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=100)
	phone = models.CharField(max_length=20, blank=True)
	is_billing = models.BooleanField(default=False)
	is_shipping = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.full_name}, {self.address_line1}, {self.city}"


class Order(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('paid', 'Paid'),
		('shipped', 'Shipped'),
		('delivered', 'Delivered'),
		('cancelled', 'Cancelled'),
		('refunded', 'Refunded'),
	]
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
	billing_address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, null=True, related_name='billing_orders')
	shipping_address = models.ForeignKey('users.Address', on_delete=models.SET_NULL, null=True, related_name='shipping_orders')
	created_at = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	payment_id = models.CharField(max_length=100, blank=True, null=True)
	payment_method = models.CharField(max_length=50, blank=True, null=True)
	refund_requested = models.BooleanField(default=False)
	refund_granted = models.BooleanField(default=False)

	def __str__(self):
		return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return f"{self.product.name} x {self.quantity}"

class Payment(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
	payment_id = models.CharField(max_length=100)
	payment_method = models.CharField(max_length=50)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=32)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Payment {self.payment_id} for Order #{self.order.id}"
