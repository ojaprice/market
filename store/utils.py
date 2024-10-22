import json
from . models import *

def cookiesCart(request):
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
    return {'items':items, 'order':order,  'cartItems': cartItems}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else: #  unauthenticated
        cookieData = cookiesCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']

    return {'items':items, 'order':order,  'cartItems': cartItems}


def visitorOrder(request, data):
    print('User not logged in.')
    print('COOKIES:', request.COOKIES)

    name = data['form']['name']
    email = data['form']['email']

    cookiesData = cookiesCart(request)
    items = cookiesData['items']

    # to store unauthorised customer data 
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name  
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
