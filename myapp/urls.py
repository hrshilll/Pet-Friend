from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# Core Pages & Authentication
urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Products
    path('products/', views.product_list, name='products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),

    # Services
    path('services/', views.service_list, name='service_list'),
    path('book-service/<int:service_id>/', views.add_service_to_cart_with_slot, name='add_service_to_cart_with_slot'),

    # Cart Management
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:cart_id>/<str:item_type>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_id>/<str:action>/', views.update_cart, name='update_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),

    # Snarkbot AI Response (Fun Addition)
    path('snarkbot-response/', views.snarkbot_response, name='snarkbot_response'),
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)