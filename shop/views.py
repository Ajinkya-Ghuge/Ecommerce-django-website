from django.shortcuts import render, get_object_or_404, redirect  # Added redirect here!
from .models import Car, Brand, Review
from django.db.models import Count
from .models import Car, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
import json

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
    



# CART VIEWS
def cart_add(request, car_id):
    """Add a car to cart"""
    car = get_object_or_404(Car, id=car_id)
    
    # Get cart from session or create new one
    cart = request.session.get('cart', {})
    
    # Convert car_id to string (session keys must be strings)
    car_id_str = str(car_id)
    
    # If car already in cart, increase quantity
    if car_id_str in cart:
        cart[car_id_str]['quantity'] += 1
        messages.success(request, f"Added another {car.brand.name} {car.name} to cart")
    else:
        # Add new item to cart
        cart[car_id_str] = {
            'id': car.id,
            'name': f"{car.brand.name} {car.name}",
            'price': float(car.daily_price),  # Convert Decimal to float for session
            'quantity': 1,
            'image': car.main_image,
            'model_year': car.model_year,
        }
        messages.success(request, f"{car.brand.name} {car.name} added to cart")
    
    # Save cart back to session
    request.session['cart'] = cart
    request.session.modified = True
    
    # FIXED: Redirect back to referring page or car detail
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('car-detail', car_id)
    

def cart_remove(request, car_id):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    car_id_str = str(car_id)
    
    if car_id_str in cart:
        car_name = cart[car_id_str]['name']
        del cart[car_id_str]
        messages.success(request, f"{car_name} removed from cart")
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_view')

def cart_update(request, car_id):
    """Update quantity of cart item"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        car_id_str = str(car_id)
        
        if car_id_str in cart:
            if quantity > 0:
                cart[car_id_str]['quantity'] = quantity
                messages.success(request, "Cart updated")
            else:
                # If quantity is 0, remove item
                del cart[car_id_str]
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart_view')

def cart_view(request):
    """Display cart page"""
    cart = request.session.get('cart', {})
    
    # Calculate totals
    cart_items = []
    subtotal = 0
    
    for item in cart.values():
        item_total = item['price'] * item['quantity']
        subtotal += item_total
        cart_items.append({
            **item,
            'total': item_total
        })
    
    # Calculate tax and grand total (10% tax example)
    tax = subtotal * 0.10
    grand_total = subtotal + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
        'cart_count': len(cart_items)
    }
    return render(request, 'shop/cart.html', context)

def checkout(request):
    """Checkout page"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, "Your cart is empty")
        return redirect('cart_view')
    
    if request.method == 'POST':
        # Process order
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        
        # Calculate total
        subtotal = 0
        for item in cart.values():
            subtotal += item['price'] * item['quantity']
        tax = subtotal * 0.10
        grand_total = subtotal + tax
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            zip_code=zip_code,
            total_amount=grand_total
        )
        
        # Create order items
        for item in cart.values():
            car = Car.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                car=car,
                quantity=item['quantity'],
                price=item['price']
            )
        
        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation', order_id=order.id)
    
    # Calculate totals for display
    subtotal = 0
    for item in cart.values():
        subtotal += item['price'] * item['quantity']
    tax = subtotal * 0.10
    grand_total = subtotal + tax
    
    context = {
        'cart_items': cart.values(),
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'shop/checkout.html', context)

def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order-confirmation.html', {'order': order})