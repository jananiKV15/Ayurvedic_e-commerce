from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Banner, Category
from random import sample
from django.contrib import messages
from .models import Product
from .models import CartItem
from .models import Cart


def home(request):
    category_id = request.GET.get('category')
    if category_id:
        all_products = Product.objects.filter(available=True, category_id=category_id)
    else:
        all_products = Product.objects.filter(available=True)

    paginator = Paginator(all_products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    banners = Banner.objects.all()
    categories = Category.objects.all()

    featured_products = Product.objects.filter(available=True, is_featured=True)
    if not featured_products.exists():
        featured_products = sample(list(all_products), min(4, len(all_products)))

    context = {
        'page_obj': page_obj,
        'banners': banners,
        'categories': categories,
        'featured_products': featured_products,
        'selected_category': int(category_id) if category_id else None,
    }
    return render(request, 'store/home.html', context)

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.subtotal() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from cart.")
    return redirect('cart')


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product)

        cart_item.quantity = quantity
        cart_item.save()

        return redirect('view_cart')


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'store/category_detail.html', {'categories': categories})



def contact_view(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\n{message}"

       

        messages.success(request, "Thanks for contacting us! We’ll get back to you soon.")
        return redirect('contact')

    return render(request, 'store/contact.html')

def category_detail_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session['cart'] = cart
    return redirect('cart')  

def cart_view(request):
    cart = request.session.get('cart', {})  
    cart_items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)  
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    context = {
        'cart_items': cart_items,
        'total': total
    }
    return render(request, 'store/cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def footer_view(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'your_template.html', {'categories': categories})

def contact_us(request):
    return render(request, 'contact.html')

def customer_support(request):
    return render(request, 'store/customer_support.html')

def search(request):
    query = request.GET.get('query', '')
    categories = Category.objects.filter(name__icontains=query) if query else Category.objects.all()
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()

    return render(request, 'store/search_results.html', {
        'query': query,
        'categories': categories,
        'products': products,
    })