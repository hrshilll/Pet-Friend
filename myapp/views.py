from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import razorpay
from .models import Product, Service, Cart, CartProduct, ServiceBooking
from .forms import CustomUserCreationForm, ServiceBookingForm
import random

def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

# ✅ Add Product to Cart (Updated)
@login_required(login_url='login')
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get("quantity", 1))

    try:
        CartProduct.add_to_cart(cart, product, quantity)
        messages.success(request, f"{product.name} added to cart!")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

# ✅ Add Service to Cart (Updated)
@login_required(login_url='login')
def add_service_to_cart_with_slot(request, service_id):
    if request.method == 'POST':
        slot = request.POST.get('preferred_slot')
        service = get_object_or_404(Service, id=service_id)

        if not slot:
            messages.warning(request, "Please select a slot before booking.")
            return redirect('service_list')

        booking = ServiceBooking.objects.create(
            user=request.user,
            service=service,
            preferred_slot=slot
        )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.service_bookings.add(booking)
        cart.services.add(service)
        cart.save()

        messages.success(request, f"Booked {service.name} at {slot}!")
        return redirect('view_cart')

    return redirect('service_list')

# ✅ Remove Product or Service from Cart
@login_required
def remove_from_cart(request, cart_id, item_type):
    cart = get_object_or_404(Cart, user=request.user)

    if item_type == "product":
        cart_product = get_object_or_404(CartProduct, id=cart_id)
        product = cart_product.product
        product.stock += cart_product.quantity
        product.save()
        cart_product.delete()
        messages.success(request, "Product removed from cart.")

    elif item_type == "service":
        booking = get_object_or_404(ServiceBooking, id=cart_id, user=request.user)
        cart.service_bookings.remove(booking)
        cart.services.remove(booking.service)
        booking.delete()
        messages.success(request, "Service booking removed from cart.")

    return redirect('view_cart')

# ✅ View Cart
@login_required
def view_cart(request):
    cart = None
    product_items = []
    service_bookings = []
    total_price = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            product_items = cart.cartproduct_set.all()
            service_bookings = cart.service_bookings.select_related('service').all()
            product_total = sum(item.total_price() for item in product_items)
            service_total = sum(booking.service.price for booking in service_bookings)
            total_price = product_total + service_total

    return render(request, 'cart.html', {
        'cart': cart,
        'product_items': product_items,
        'service_bookings': service_bookings,
        'total_price': total_price
    })

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

# ✅ Update Cart
@login_required
def update_cart(request, cart_id, action):
    cart_product = get_object_or_404(CartProduct, id=cart_id)
    product = cart_product.product

    if action == "increase":
        cart_product.quantity += 1
        product.stock -= 1
        product.save()

    elif action == "decrease":
        cart_product.quantity -= 1
        product.stock += 1
        product.save()

        if cart_product.quantity <= 0:
            cart_product.delete()
            return redirect('view_cart')

    cart_product.save()
    return redirect('view_cart')

# ✅ Checkout
@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_products = cart.cartproduct_set.all()
    cart_services = cart.services.all()

    total_price = sum(item.total_price() for item in cart_products) + sum(service.price for service in cart.services.all())

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

    razorpay_order = client.order.create({
        "amount": int(total_price * 100),
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "checkout.html", {
        "cart_products": cart_products,
        "cart_services": cart_services,
        "total_price": total_price,
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })

# ✅ Service List
def service_list(request):
    services = Service.objects.all()
    form = ServiceBookingForm()

    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Service booked successfully!')
            return redirect('view_cart')

    cart_count = request.session.get('cart_count', 0)

    return render(request, 'service_list.html', {
        'services': services,
        'form': form,
        'cart_count': cart_count
    })

# ✅ Product List
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

# ✅ Signup
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# ✅ Custom Login with Message Clear
from django.contrib.messages import get_messages

def user_login(request):
    list(get_messages(request))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")

# ✅ Custom Logout with Message Clear
def user_logout(request):
    logout(request)
    list(get_messages(request))
    messages.success(request, "Logged out successfully.")
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def snarkbot_response(request):
    snarks = [
        "Oh wow, someone’s feeling spendy today.",
        "Adding more? Your wallet’s crying.",
        "This cart is getting *thicc*.",
        "You're not adopting all of Petco, right?",
        "Better make space in the trunk.",
    ]
    return JsonResponse({"snark": random.choice(snarks)})
