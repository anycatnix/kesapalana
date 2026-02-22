from django.contrib import admin
from .models import Testimonial, NewsletterSubscriber, HeroSection, SiteSettings

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ("name", "rating", "featured", "created_at")
	list_filter = ("featured", "rating")
	search_fields = ("name", "content")

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
	list_display = ("email", "subscribed_at")
	search_fields = ("email",)

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
	list_display = ("headline", "cta_text")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
	list_display = ("site_name", "contact_email")
