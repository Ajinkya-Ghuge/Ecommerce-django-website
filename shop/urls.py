from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all-cars/', views.all_cars, name='all-cars'),
    path('car/<int:car_id>/', views.car_detail, name='car-detail'),
    path('technical-specs/<int:car_id>/', views.technical_specs, name='technical-specs'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.category_cars, name='category-cars'),
]