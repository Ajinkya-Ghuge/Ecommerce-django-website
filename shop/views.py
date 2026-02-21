from django.shortcuts import render, get_object_or_404
from .models import Car, Brand, Review
from django.db.models import Count

def home(request):
    bestselling_car = Car.objects.filter(is_bestselling=True).first()
    featured_cars = Car.objects.filter(is_featured=True).order_by('?')[:6]
    brands = Brand.objects.all()
    latest_reviews = Review.objects.all().order_by('-date')[:4]
    
    # Get counts for each category
    economy_count = Car.objects.filter(category='economy').count()
    exotic_count = Car.objects.filter(category='exotic').count()
    sport_count = Car.objects.filter(category='sport').count()
    luxury_count = Car.objects.filter(category='luxury').count()
    suv_count = Car.objects.filter(category='suv').count()
    
    context = {
        'bestselling_car': bestselling_car,
        'featured_cars': featured_cars,
        'brands': brands,
        'latest_reviews': latest_reviews,
        'economy_count': economy_count,
        'exotic_count': exotic_count,
        'sport_count': sport_count,
        'luxury_count': luxury_count,
        'suv_count': suv_count,
    }
    return render(request, 'shop/home.html', context)

def all_cars(request):
    cars = Car.objects.all().order_by('-created_at')
    context = {
        'cars': cars,
    }
    return render(request, 'shop/all-cars.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = car.reviews.all()[:3]
    similar_cars = Car.objects.filter(category=car.category).exclude(id=car.id)[:3]
    
    context = {
        'car': car,
        'reviews': reviews,
        'similar_cars': similar_cars,
    }
    return render(request, 'shop/car-detail.html', context)

def technical_specs(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    all_cars = Car.objects.all()[:5]
    context = {
        'car': car,
        'all_cars': all_cars,
    }
    return render(request, 'shop/technical-specs.html', context)

def search(request):
    query = request.GET.get('q', '')
    if query:
        cars = Car.objects.filter(name__icontains=query) | Car.objects.filter(brand__name__icontains=query)
    else:
        cars = Car.objects.none()
    
    context = {
        'cars': cars,
        'query': query,
    }
    return render(request, 'shop/search-results.html', context)

def category_cars(request, category):
    cars = Car.objects.filter(category=category)
    context = {
        'cars': cars,
        'current_category': category,
    }
    return render(request, 'shop/all-cars.html', context)