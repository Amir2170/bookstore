from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

from .models import Cart
from shop.models import Product


def add(request, slug):
    cart =  request.session.get('cart', {})
    product = Product.objects.get(slug=slug)
    
    if slug not in cart:
        cart[slug] = {'price': str(product.price)}
        request.session['cart'] = cart
    
    request.session.modified = True
    
    return HttpResponse("Added")
    