from django.shortcuts import render
from .models import Product, Order, Customer, OrderItem, ShippingAddress
# step3 
from django.http import JsonResponse
import json

from datetime import datetime

# DRY 
from .utils import cookiesCart, cartData, visitorOrder


# Create your views here.
# Ensuring DRY principle
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems,}
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
    cartItems = data['cartItems']
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items':items, 'order':order,  'cartItems': cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
            
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, "store/checkout.html", context)


# To add to cart   
def updateItem(request):
    # data sent from the frontend 
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('ProductId', productId)
    print('Action', action)

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
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Successful', safe=False)


