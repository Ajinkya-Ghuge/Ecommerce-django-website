from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Car(models.Model):
    FUEL_TYPES = [
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    TRANSMISSION_TYPES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('semi-auto', 'Semi-Automatic'),
    ]
    
    DRIVETRAIN_TYPES = [
        ('fwd', 'FWD'),
        ('rwd', 'RWD'),
        ('awd', 'AWD'),
        ('4wd', '4WD'),
    ]
    
    CATEGORY_CHOICES = [
        ('economy', 'Economy Cars'),
        ('exotic', 'Exotic Cars'),
        ('sport', 'Sport Cars'),
        ('luxury', 'Luxury Cars'),
        ('suv', 'SUV\'s'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    model_year = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Pricing
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    msrp_range = models.CharField(max_length=50, blank=True)
    
    # Specifications
    seats = models.IntegerField(default=5)
    engine = models.CharField(max_length=100)
    power = models.CharField(max_length=50)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES)
    drivetrain = models.CharField(max_length=10, choices=DRIVETRAIN_TYPES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    consumption = models.CharField(max_length=50, blank=True)
    
    # Features
    features = models.TextField(help_text="Enter each feature on a new line")
    
    # Images
    main_image = models.URLField(max_length=500)
    interior_image = models.URLField(max_length=500, blank=True)
    exterior_image = models.URLField(max_length=500, blank=True)
    
    # Overview
    overview = models.TextField()
    is_bestselling = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.model_year})"
    
    def get_absolute_url(self):
        return reverse('car-detail', args=[str(self.id)])
    
    def get_features_list(self):
        return self.features.split('\n')

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='additional_images')
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True)

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100, default="Auto Expert")
    
    def __str__(self):
        return f"{self.car.name} - {self.title}"