from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category_view, name='category'),
    path('category/<int:category_id>/', views.category_detail_view, name='category_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('customer-support/', views.customer_support, name='customer_support'),
    path('search/', views.search, name='search'),
    path('accounts/', include('accounts.urls')),
]

