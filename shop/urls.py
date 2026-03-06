from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all-cars/', views.all_cars, name='all-cars'),
    path('car/<int:car_id>/', views.car_detail, name='car-detail'),
    path('technical-specs/<int:car_id>/', views.technical_specs, name='technical-specs'),
    path('search/', views.search, name='search'),
    path('category/<str:category>/', views.category_cars, name='category-cars'),




        # CART URLs (ADD THESE)
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:car_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:car_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:car_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]