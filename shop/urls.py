from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Product listing
    path('products/', views.product_list, name='product_list'),
    path('products/<int:category_id>/', views.product_list, name='product_list_category'),

    # Product detail
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Direct SSLCommerz checkout from cart
    path('ssl-checkout/', views.ssl_checkout, name='ssl_checkout'),

    # SSLCommerz payment page
    path('ssl-payment/<int:invoice_id>/', views.ssl_payment, name='ssl_payment'),

    # Categories Page (Listing all categories)
    path('categories/', views.categories_view, name='categories'),

    # Contact page
    path('contact/', views.contact_view, name='contact'),

    # Search page
    path('search/', views.search_view, name='search'),
]
