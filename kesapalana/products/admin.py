from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ("name", "slug", "featured")
	search_fields = ("name",)

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1

class ProductVariantInline(admin.TabularInline):
	model = ProductVariant
	extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ("name", "category", "price", "featured", "inventory")
	list_filter = ("category", "featured")
	search_fields = ("name", "slug")
	inlines = [ProductImageInline, ProductVariantInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
	list_display = ("product", "name", "value", "price", "inventory")

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
	list_display = ("product", "alt_text")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ("product", "user", "rating", "created_at")
