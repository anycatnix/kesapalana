from django.contrib import admin
from .models import Order, OrderItem, Payment, Address

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'status', 'created_at', 'total', 'refund_requested', 'refund_granted')
	list_filter = ('status', 'refund_requested', 'refund_granted')
	search_fields = ('user__username', 'id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ('order', 'payment_id', 'payment_method', 'amount', 'status', 'created_at')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display = ('user', 'full_name', 'city', 'country', 'is_billing', 'is_shipping')
