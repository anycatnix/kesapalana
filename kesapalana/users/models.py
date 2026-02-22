
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	# Add any extra fields here
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	phone = models.CharField(max_length=20, blank=True)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	bio = models.TextField(blank=True)
	location = models.CharField(max_length=100, blank=True)
	website = models.URLField(blank=True)

	def __str__(self):
		return f"Profile of {self.user.username}"

class Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
	full_name = models.CharField(max_length=100)
	address_line1 = models.CharField(max_length=255)
	address_line2 = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	country = models.CharField(max_length=100)
	phone = models.CharField(max_length=20, blank=True)
	is_default = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.full_name}, {self.address_line1}, {self.city}"

class Wishlist(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
	products = models.ManyToManyField('products.Product', blank=True)

	def __str__(self):
		return f"Wishlist of {self.user.username}"
