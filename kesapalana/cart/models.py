from django.db import models
from django.conf import settings
from products.models import Product
import uuid
from decimal import Decimal

class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True)
	discount_percent = models.PositiveIntegerField(default=0)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.code

class Cart(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
	coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def subtotal(self):
		return sum(item.total_price() for item in self.items.all())

	def discount(self):
		if self.coupon and self.coupon.active:
			return self.subtotal() * (self.coupon.discount_percent / 100)
		return 0

	from decimal import Decimal
	def tax(self):
		return self.subtotal() * Decimal('0.18')  # 18% GST example

	def shipping(self):
		return 50 if self.subtotal() < 1000 else 0

	def total(self):
		return self.subtotal() - self.discount() + self.tax() + self.shipping()

	def __str__(self):
		return f"Cart for {self.user.username if self.user else 'Session'}"

class CartItem(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	def total_price(self):
		return self.product.price * self.quantity

	def __str__(self):
		return f"{self.product.name} x {self.quantity}"
