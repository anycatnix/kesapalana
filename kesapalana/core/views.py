def success_stories_page(request):
	# Dummy data for now; replace with real model/query if available
	stories = [
		{'name': 'Arjun K.', 'content': 'I saw real results in 3 months!'},
		{'name': 'Vikram S.', 'content': 'My hair feels thicker and healthier.'},
		{'name': 'Rahul M.', 'content': 'Finally a brand that focuses just on men\'s hair.'},
	]
	return render(request, 'core/success_stories.html', {'stories': stories})

def ingredients_page(request):
	# Dummy data for now; replace with real model/query if available
	ingredients = [
		{'name': 'Bhringraj', 'description': 'Promotes hair growth and reduces hair fall.'},
		{'name': 'Amla', 'description': 'Rich in Vitamin C, strengthens hair follicles.'},
		{'name': 'Minoxidil', 'description': 'Clinically proven to help regrow hair.'},
		{'name': 'Biotin', 'description': 'Supports healthy hair and scalp.'},
	]
	return render(request, 'core/ingredients.html', {'ingredients': ingredients})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Testimonial, NewsletterSubscriber, HeroSection, SiteSettings
from .forms import NewsletterForm, ContactForm

def home(request):
	hero = HeroSection.objects.first()
	testimonials = list(Testimonial.objects.filter(featured=True)[:3])
	if not testimonials:
		testimonials = [
			type('obj', (object,), {'name': 'Arjun K.', 'content': 'I saw real results in 3 months!'}),
			type('obj', (object,), {'name': 'Vikram S.', 'content': 'My hair feels thicker and healthier.'}),
			type('obj', (object,), {'name': 'Rahul M.', 'content': 'Finally a brand that focuses just on men\'s hair.'}),
		]
	settings = SiteSettings.objects.first()
	return render(request, 'core/home.html', {
		'hero': hero,
		'testimonials': testimonials,
		'settings': settings,
	})

def science_page(request):
	settings = SiteSettings.objects.first()
	return render(request, 'core/science.html', {'settings': settings})

def about_page(request):
	settings = SiteSettings.objects.first()
	return render(request, 'core/about.html', {'settings': settings})

def testimonials_page(request):
	testimonials = Testimonial.objects.all()
	return render(request, 'core/testimonials.html', {'testimonials': testimonials})

def contact_page(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			# Here you would send an email or save the message
			messages.success(request, 'Thank you for contacting us!')
			return redirect('core:contact')
	else:
		form = ContactForm()
	return render(request, 'core/contact.html', {'form': form})

def subscribe_newsletter(request):
	if request.method == 'POST':
		form = NewsletterForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			NewsletterSubscriber.objects.get_or_create(email=email)
			messages.success(request, 'Subscribed to newsletter!')
			return redirect(request.META.get('HTTP_REFERER', '/'))
	else:
		form = NewsletterForm()
	return render(request, 'core/subscribe_newsletter.html', {'form': form})
