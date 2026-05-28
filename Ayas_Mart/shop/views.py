from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product

# 1. होमपेज (सामान दिखाने और सर्च के लिए)
def home(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# 2. यूजर रजिस्ट्रेशन (नया अकाउंट बनाना)
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "भाई साहब, यह यूजरनेम पहले से मौजूद है!")
            return redirect('register')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user) # अकाउंट बनते ही ऑटोमैटिक लॉगिन कर देगा
        messages.success(request, "आपका अकाउंट सफलतापूर्वक बन गया है!")
        return redirect('home')
    return render(request, 'register.html')

# 3. यूजर लॉगिन (पुराने अकाउंट में घुसना)
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "लॉगिन सफल रहा!")
            return redirect('home')
        else:
            messages.error(request, "गलत यूजरनेम या पासवर्ड! कृपया दोबारा जाँचें।")
            return redirect('login')
    return render(request, 'login.html')

# 4. यूजर लॉगआउट (अकाउंट से बाहर निकलना)
def logout_view(request):
    logout(request)
    messages.success(request, "आप सफलतापूर्वक लॉगआउट हो गए हैं।")
    return redirect('home')

# 5. कार्ट में सामान जोड़ना
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image_url': product.image.url if product.image else ''
        }
        
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart_detail')

# 6. कार्ट से सामान हटाना
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('cart_detail')

# 7. कार्ट का पेज देखना
def cart_detail(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

# 8. चेकआउट पेज (अब सिर्फ लॉगिन यूजर ही देख सकते हैं)
@login_required(login_url='login')
def checkout(request):
    return render(request, 'checkout.html')

# 9. ऑर्डर सक्सेस पेज
@login_required(login_url='login')
def order_success(request):
    cart = request.session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
        
    return render(request, 'order_success.html', {'total_price': total_price})