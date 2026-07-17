from urllib import request

from django.shortcuts import render, redirect
from .models import Product, Order, OrderHistory, Wishlist, Address
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
import random
from django.http import JsonResponse

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

    categories = Product.objects.values_list(
        'category', flat=True
    ).distinct()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔥 NAYA - Cart items fetch karo
    cart_items = {}
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        cart_items = {order.product.id: order for order in orders}

    return render(request, 'products.html', {
        'products': page_obj,
        'categories': categories,
        'cart_items': cart_items,  # 🔥 NAYA
    })


# 🔥 CART


def cart(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    orders = Order.objects.filter(user=request.user)
    total = sum([order.product.price * order.quantity for order in orders])

    return render(request, "cart.html", {"orders": orders, "total": total})


# 🔥 ADD TO CART
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'login'})
        return redirect('/login/')

    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        order.quantity += 1
        order.save()

    # 🔥 AJAX request hai toh JSON do
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'qty': order.quantity,
            'order_id': order.id
        })
    return redirect('/')




# 🔥 INCREASE
def increase_quantity(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    order.quantity += 1
    order.save()

    # 🔥 AJAX request hai toh JSON do
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'qty': order.quantity})
    return redirect('/')

# 🔥 DECREASE
def decrease_quantity(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.quantity > 1:
        order.quantity -= 1
        order.save()
        qty = order.quantity
    else:
        order.delete()
        qty = 0  # 🔥 Zero pe delete

    # 🔥 AJAX request hai toh JSON do
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'qty': qty})
    return redirect('/')

# 🔥 REMOVE
def remove_item(request, order_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "login"}, status=401)

    order = Order.objects.get(id=order_id, user=request.user)
    order.delete()
    return JsonResponse({"removed": True})


# 🔥 SIGNUP
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match ❌")
            return redirect("/signup/")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect("/signup/")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("/")

    return render(request, "signup.html")


# 🔥 CHECKOUT


# 🔥 CHECKOUT
def checkout(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    orders = Order.objects.filter(user=request.user)

    if not orders.exists():
        messages.error(request, "Your cart is empty 😢")
        return redirect("/cart/")

    addresses = Address.objects.filter(user=request.user)
    total = sum(order.product.price * order.quantity for order in orders)

    if request.method == "POST":

        selected_address_id = request.POST.get("selected_address")

        if not selected_address_id:
            messages.error(request, "Please select an address 😢")
            return redirect("/checkout/")

        address = Address.objects.get(id=selected_address_id, user=request.user)
        order_id = random.randint(100000, 999999)

        for order in orders:
            OrderHistory.objects.create(
                user=request.user,
                product_name=order.product.name,
                price=order.product.price,
                quantity=order.quantity,
                delivery_name=address.full_name,
                delivery_mobile=address.mobile,
                delivery_house=address.house_no,
                delivery_street=address.street,
                delivery_city=address.city,
                delivery_state=address.state,
                delivery_pincode=address.pincode,
            )

        orders.delete()
        return render(request, "success.html", {"random_id": order_id})

    # GET request — show the checkout page
    return render(
        request,
        "checkout.html",
        {"orders": orders, "total": total, "addresses": addresses},
    )

    total = sum([order.product.price * order.quantity for order in orders])

    return render(request, "checkout.html", {"orders": orders, "total": total})


# 🔥 ORDERS


def order_history(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    orders = OrderHistory.objects.filter(user=request.user)

    return render(request, "orders.html", {"orders": orders})


# 🔥 PRODUCT DETAIL


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, "product_detail.html", {"product": product})


# 🔥 WISHLIST


def add_to_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)

    return redirect("/")


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    items = Wishlist.objects.filter(user=request.user)

    return render(request, "wishlist.html", {"items": items})


def remove_from_wishlist(request, id):
    item = Wishlist.objects.get(id=id, user=request.user)
    item.delete()
    return redirect("/wishlist/")


def set_default_address(request, id):

    if not request.user.is_authenticated:
        return redirect("/login/")

    Address.objects.filter(user=request.user).update(is_default=False)

    address = Address.objects.get(id=id, user=request.user)

    address.is_default = True
    address.save()

    return redirect("/addresses/")


def delete_address(request, id):

    if not request.user.is_authenticated:
        return redirect("/login/")

    address = Address.objects.get(id=id, user=request.user)

    address.delete()

    return redirect("/addresses/")


def manage_addresses(request):

    if not request.user.is_authenticated:
        return redirect("/login/")

    if request.method == "POST":

        Address.objects.create(
            user=request.user,
            full_name=request.POST["full_name"],
            mobile=request.POST["mobile"],
            house_no=request.POST["house_no"],
            street=request.POST["street"],
            city=request.POST["city"],
            state=request.POST["state"],
            pincode=request.POST["pincode"],
        )

        return redirect("/addresses/")

    addresses = Address.objects.filter(user=request.user)

    return render(request, "addresses.html", {"addresses": addresses})


# 🔥 CANCEL ORDER
# 🔥 CANCEL ORDER
def cancel_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    order = OrderHistory.objects.get(id=order_id, user=request.user)

    if order.status == "Pending":
        order.status = "Cancelled"
        order.cancel_reason = "Cancelled by customer."
        order.save()
        messages.success(
            request, f"Order for '{order.product_name}' has been cancelled."
        )
    else:
        messages.error(request, "This order cannot be cancelled.")

    return redirect("/orders/")
