from ast import Or
import datetime
from urllib import response
from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests import request
from carts.models import Cart, CartItem
from orders.forms import OrderForm
from store.models import Product
from .models import Order, OrderProduct, Payment
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
def payments(request):
    if request.method == 'POST':
        order_number = request.POST['order_number']
        total = request.POST['total']
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
        
        # Store transaction details inside payment model
        payment = Payment(
            user = request.user,
            payment_id = order_number,
            payment_method = 'COD',
            amount_paid = order.order_total,
            status = 'COMPLETED',
        )
        payment.save()
        
        order.payment = payment
        order.is_ordered = True
        order.save()
        
        # Move the cart items to order product table
        cart_items = CartItem.objects.filter(user=request.user)
        
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()
            
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
            
            # Replace the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
        
        # clear Cart
        CartItem.objects.filter(user=request.user).delete()
        # send order received email to customer
        mail_subject = 'Thank you for order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order':order
        }) 
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        # Send order number to transaction
        
    return render(request, 'orders/payments.html')



def place_order(request, total = 0, quantity = 0):
    current_user = request.user
    print(current_user)
    # if the cart count is less than or equal to 0, than redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() 
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False,order_number= order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,
            }
            return render(request,'orders/payments.html',context)
        else:
            return HttpResponse('Problem ')
    else:
        return redirect('checkout')
    
