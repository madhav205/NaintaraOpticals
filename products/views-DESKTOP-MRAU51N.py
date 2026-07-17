from django.shortcuts import render, redirect
from .models import Product, Order, OrderHistory, Wishlist
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Address
from django.contrib.auth.models import User
import random

# 🔥 HOME PAGE

def product_list(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    category = request.GET.get('category')
    if category:
        products = products.filter(category__icontains=category)

    sort = request.GET.get('sort')
    if sort == 'low':
        products = products.order_by('price')
    elif sort == 'high':
        products = products.order_by('-price')

    categories = Product.objects.values_list('category', flat=True).distinct()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': page_obj,
        'categories': categories
    })


# 🔥 CART

def cart(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    orders = Order.objects.filter(user=request.user)
    total = sum([order.product.price * order.quantity for order in orders])

    return render(request, 'cart.html', {
        'orders': orders,
        'total': total
    })


# 🔥 ADD TO CART

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    product = Product.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        order.quantity += 1
        order.save()

    return redirect('/')


# 🔥 INCREASE

def increase_quantity(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.quantity += 1
    order.save()
    return redirect('/cart/')


# 🔥 DECREASE

def decrease_quantity(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    if order.quantity > 1:
        order.quantity -= 1
        order.save()
    return redirect('/cart/')


# 🔥 REMOVE

def remove_item(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.delete()
    return redirect('/cart/')


# 🔥 SIGNUP

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('/signup/')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, 'signup.html')


# 🔥 CHECKOUT

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    orders = Order.objects.filter(user=request.user)

    if not orders.exists():
        messages.error(request, "Your cart is empty 😢")
        return redirect('/cart/')

    if request.method == 'POST':
        order_id = random.randint(100000, 999999)

        for order in orders:
            OrderHistory.objects.create(
                user=request.user,
                product_name=order.product.name,
                price=order.product.price,
                quantity=order.quantity
            )

        orders.delete()

        return render(request, 'success.html', {
            'random_id': order_id
        })

    total = sum([order.product.price * order.quantity for order in orders])

    return render(request, 'checkout.html', {
        'orders': orders,
        'total': total
    })


# 🔥 ORDERS

def order_history(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    orders = OrderHistory.objects.filter(user=request.user)

    return render(request, 'orders.html', {'orders': orders})


# 🔥 PRODUCT DETAIL

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})


# 🔥 WISHLIST

def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect('/login/')

    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)

    return redirect('/')


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {'items': items})


def remove_from_wishlist(request, id):
    item = Wishlist.objects.get(id=id, user=request.user)
    item.delete()
    return redirect('/wishlist/')
def manage_addresses(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    if request.method == 'POST':

        Address.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            mobile=request.POST['mobile'],
            house_no=request.POST['house_no'],
            street=request.POST['street'],
            city=request.POST['city'],
            state=request.POST['state'],
            pincode=request.POST['pincode']
            
        )

        return redirect('/addresses/')

    addresses = Address.objects.filter(user=request.user)
    

    return render(
        request,
        'addresses.html',
        {'addresses': addresses}
    )