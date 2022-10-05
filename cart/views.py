from django.shortcuts import render, redirect, get_object_or_404
from Appointments.models import Service
from .cart import Cart
from .forms import CartAddServiceForm


# Create your views here.

def cart_add(request, service_id):
    cart = Cart (request)
    service = get_object_or_404 (Service, id=service_id)
    cart.add (
        service=service,
        quantity=1
    )

    print(service.name)
    print(cart.get_total_price())

    return redirect ('appointments:service_list')  # simply redirect to the page displaying our services.


def cart_remove(request, service_id):
    cart = Cart (request)
    service = get_object_or_404 (Service, id=service_id)
    cart.remove (service)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart (request)
    for item in cart:
        item['update_quantity_form'] = CartAddServiceForm (
            initial={
                'quantity': item['quantity'],
                'update': True
            }
        )
    return render (request, 'cart/detail.html', {'cart': cart})
