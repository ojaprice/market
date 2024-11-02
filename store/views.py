from django.shortcuts import render, redirect
from .models import Product, Order, Customer, OrderItem, ShippingAddress
from django.contrib.auth import login, authenticate
from django.contrib import messages

# step3
from django.http import JsonResponse
import json

from datetime import datetime

# DRY
from .utils import cookiesCart, cartData, visitorOrder

from .forms import RegistrationForm, LoginForm


# Authentication
# register 
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success("Account Successfully Created")
            return redirect("/store")
    else:
        form = RegistrationForm()
        # messages
    return render(request, "registration/register.html", {"form": form})


# from django.contrib.auth.views import LoginView

# class CustomLoginView(LoginView):
#     template_name = 'registration/login.html'

# login
# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username'] 
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # messages.success(request, "Login successful")
#             return redirect('/store')
#         else:
#             messages.error(request, "Invalid username or password")
#     return render(request, "registration/login.html")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Optionally, display a success message
                # messages.success(request, "Login successful")
                return redirect('/store')  # Replace with your desired redirect path
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


# Ensuring DRY principle
def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]

    products = Product.objects.all()
    context = {
        "products": products,
        "cartItems": cartItems,
    }
    return render(request, "store/store.html", context)


def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    # else: #  unauthenticated
    #     cookieData = cookiesCart(request)
    #     cartItems = cookieData['cartItems']
    #     items = cookieData['items']
    #     order = cookieData['order']

    data = cartData(request)
    cartItems = data["cartItems"]
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    cartItems = data["cartItems"]
    items = data["items"]
    order = data["order"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


# To add to cart
def updateItem(request):
    # data sent from the frontend
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("ProductId", productId)
    print("Action", action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # total = float(data['form']['total'])
        # order.transaction_id = transaction_id

    else:
        customer, order = visitorOrder(request, data)
    # available for both users
    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment Successful", safe=False)
