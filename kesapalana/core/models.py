from django.db import models

class Testimonial(models.Model):
	name = models.CharField(max_length=100)
	content = models.TextField()
	rating = models.PositiveIntegerField(default=5)
	created_at = models.DateTimeField(auto_now_add=True)
	featured = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.name} ({self.rating}/5)"

class NewsletterSubscriber(models.Model):
	email = models.EmailField(unique=True)
	subscribed_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email

class HeroSection(models.Model):
	headline = models.CharField(max_length=255)
	subheadline = models.CharField(max_length=255, blank=True)
	background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
	cta_text = models.CharField(max_length=100, blank=True)
	cta_link = models.URLField(blank=True)

	def __str__(self):
		return self.headline

class SiteSettings(models.Model):
	site_name = models.CharField(max_length=100)
	seo_title = models.CharField(max_length=255, blank=True)
	seo_description = models.TextField(blank=True)
	contact_email = models.EmailField(blank=True)
	contact_phone = models.CharField(max_length=20, blank=True)
	address = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.site_name
