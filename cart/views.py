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
    view_messages = {
        'uable_to_del': _('unable to delete given product')
    }
    
    if user.is_authenticated:
        product = Product.objects.get(slug=slug)    
        
        try: 
            result = product.delete()
        except Exception as e:   
            if result == 0:
                messages.error(request, 
                    view_messages['unable_to_del']
                )
            else:
                raise e
    
    else:       
        cart = request.session['cart']
       
        try:
            del cart['slug']
        except Exception as e:
            if e == NameError:
                messages.error(request, 
                    view_messages['unable_to_del']
                )
            else:
                raise e
    
    return redirect('shop:home')
        
        