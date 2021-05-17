from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST

from .models import Cart
from shop.models import Product


def detail(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = {}
    else:
        cart = request.session.get('cart', {})
    
    return render(request, 'detail.html', 
        {'cart': cart}
    )
        


def add(request, slug):
    product = Product.objects.get(slug=slug)
    view_messages = {
        'adding_twice': _("Already added"),
        'successfully_added': _(
            "Product added successfully"
        ),
    }
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        
        if product not in cart.products.all():
            cart.products.add(product)
        else:
            messages.error(request, 
                view_messages['adding_twice']
            )
            return redirect(reverse('shop:home'))
    
    else:
        cart =  request.session.get('cart', {})

        if slug not in cart:
            cart[slug] = {'price': str(product.price)} 
            request.session['cart'] = cart
        else:
            messages.error(request, 
                view_messages['adding_twice']
            )
            return redirect(reverse('shop:home'))
        
        request.session.modified = True
    
    messages.success(request, 
        view_messages['successfully_added']
    )
    return redirect(reverse('shop:home'))



def remove(request, slug):
    product = Product.objects.get(slug=slug)
    
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
    
    else:
        cart = request.session.get('cart')
        del cart[product.slug]
        request.session.modified = True
    
    messages.success(request, 
        _("Product removed successfully from your cart"))
    
    return redirect(reverse('shop:home'))
        
        
        