from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# ✅ Service Model
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Grooming', 'Grooming'),
        ('Health', 'Health'),
        ('Home', 'Home'),
        ('Training', 'Training'),
        ('Lifestyle', 'Lifestyle'),
    ]

    SLOT_CHOICES = [
        ('07:00 - 08:00', '07:00 - 08:00'),
        ('08:00 - 09:00', '08:00 - 09:00'),
        ('09:00 - 10:00', '09:00 - 10:00'),
        ('10:00 - 11:00', '10:00 - 11:00'),
        ('11:00 - 12:00', '11:00 - 12:00'),
        ('12:00 - 13:00', '12:00 - 13:00'),
        ('13:00 - 14:00', '13:00 - 14:00'),
        ('14:00 - 15:00', '14:00 - 15:00'),
        ('15:00 - 16:00', '15:00 - 16:00'),
        ('16:00 - 17:00', '16:00 - 17:00'),
        ('17:00 - 18:00', '17:00 - 18:00'),
        ('18:00 - 19:00', '18:00 - 19:00'),
    ]

    preferred_slot = models.CharField(max_length=20, choices=SLOT_CHOICES, blank=True, null=True)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name

class ServiceBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    preferred_slot = models.CharField(max_length=50)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.service.name} at {self.preferred_slot}"

# ✅ Custom User Model
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=20, choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')])
    pet_breed = models.CharField(max_length=50)
    pet_age = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    pet_gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
   
    def __str__(self):
        return self.username

# ✅ Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)  # stock/limit field

    def __str__(self):
        return self.name

# ✅ Cart Model (Now Supports Multiple Products & Services)
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)  # Track services separately
    service_bookings = models.ManyToManyField(ServiceBooking, blank=True)  # Track slot bookings

    def total_price(self):
        product_total = sum(item.total_price() for item in self.cartproduct_set.all())  # Sum of all product prices
        service_total = sum(service.price for service in self.services.all())  # Sum of all service prices
        return product_total + service_total

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Guest'}"

# ✅ CartProduct Model (For Tracking Products & Quantities in Cart)
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def reduce_stock(self):
        if self.product.stock >= self.quantity:
            self.product.stock -= self.quantity
            self.product.save()
        else:
            raise ValueError(f"Only {self.product.stock} left in stock for '{self.product.name}'")
        
     

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def delete(self, *args, **kwargs):
        # Auto-restock on delete
        self.product.stock += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    @classmethod
    def add_to_cart(cls, cart, product, quantity):
        product.refresh_from_db()

        if product.stock <= 0:
            raise ValueError(f"{product.name} is out of stock.")

        if product.stock < quantity:
            raise ValueError(f"Only {product.stock} items available for '{product.name}'.")

        cart_product, created = cls.objects.get_or_create(cart=cart, product=product)

        cart_product.quantity += quantity
        cart_product.save()

        product.stock -= quantity
        product.save()

        return cart_product