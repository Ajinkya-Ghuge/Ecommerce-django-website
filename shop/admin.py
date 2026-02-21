from django.contrib import admin
from .models import Brand, Car, CarImage, Review

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'model_year', 'category', 'daily_price', 'is_bestselling']
    list_filter = ['brand', 'category', 'fuel_type', 'drivetrain', 'is_bestselling']
    search_fields = ['name', 'brand__name']
    list_editable = ['daily_price', 'is_bestselling']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'brand', 'model_year', 'category')
        }),
        ('Pricing', {
            'fields': ('daily_price', 'purchase_price', 'msrp_range')
        }),
        ('Specifications', {
            'fields': ('seats', 'engine', 'power', 'transmission', 'drivetrain', 'fuel_type', 'consumption')
        }),
        ('Features & Media', {
            'fields': ('features', 'main_image', 'interior_image', 'exterior_image')
        }),
        ('Description', {
            'fields': ('overview',)
        }),
        ('Settings', {
            'fields': ('is_bestselling', 'is_featured')
        }),
    )

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'alt_text']
    list_filter = ['car']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['car', 'title', 'date']
    list_filter = ['car', 'date']
    search_fields = ['title', 'content']