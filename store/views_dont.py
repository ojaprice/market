from django.shortcuts import render
from .models import Product, Order, Customer, OrderItem, ShippingAddress
# step3 
from django.http import JsonResponse
import json

from datetime import datetime


# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems,}
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else: #  unauthenticated
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print("Cart:", cart)


        items = [] #to store items for unauthentiated user
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

        for i in cart:
            # error: Incase product is deleted from the database
            try:
                cartItems += cart[i]['quantity']
            
                # build order 
                product = Product.objects.get(id=i)
                total = product.price * cart[i]['quantity']
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                        },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                    }
                items.append(item)

                # digital product 
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    context = {'items':items, 'order':order,  'cartItems': cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    
    context = {'items':items, 'order':order}
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
        total = float(data['form']['total'])

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
    else:
        print('User not logged in.')
    return JsonResponse('Payment Successful', safe=False)


