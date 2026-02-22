from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product, Category, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def product_list(request):
	category_slug = request.GET.get('category')
	search_query = request.GET.get('q')
	products = Product.objects.all()
	categories = Category.objects.all()
	if category_slug:
		products = products.filter(category__slug=category_slug)
	if search_query:
		products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
	return render(request, 'products/product_list.html', {
		'products': products,
		'categories': categories,
		'selected_category': category_slug,
		'search_query': search_query,
	})

def product_detail(request, slug):
	product = get_object_or_404(Product, slug=slug)
	reviews = product.reviews.select_related('user').all()
	return render(request, 'products/product_detail.html', {
		'product': product,
		'reviews': reviews,
	})

@login_required
def add_review(request, slug):
	product = get_object_or_404(Product, slug=slug)
	if request.method == 'POST':
		rating = int(request.POST.get('rating', 5))
		comment = request.POST.get('comment', '')
		Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
		messages.success(request, 'Review submitted!')
		return redirect('products:product_detail', slug=slug)
	return render(request, 'products/add_review.html', {'product': product})
