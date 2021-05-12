from django.template import Template, Context
from django.test import TestCase
from django.urls import reverse

from cart.models import Cart
from shop.models import Product, Category
from .functions import(
     _create_product_and_category_in_database,
)


class CartTotalPriceTagTest(TestCase):
    
    TEMPLATE = Template("{% load cart_total_price %} {% cart_total_price %}")
    
    def test_cart_total_price_shows_up(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', price=1000.20
        )
        product2 = _create_product_and_category_in_database(
            product_name='product2', price=2000.30
        )
        
        self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )
        self.client.post(reverse('cart:add', 
            args=[product2.slug],), follow=True,
        )
        
        session = self.client.session
            
        rendered = self.TEMPLATE.render(Context(
            {'cart': session['cart']}
            )
        )
        
        self.assertIn('3000.50', rendered)
        
     