from django.test import TestCase
from django.urls import reverse

from cart.models import Cart
from shop.models import Product, Category
		

class TestAddView(TestCase):

    def _create_product_and_category_in_database(self, product_name,
        price=100):
	    category = Category.objects.create(
		    name='category',
		    slug=product_name + 'category',
		    is_sub=False,
		)
	    product = Product.objects.create(
		    name=product_name,
		    author='author',
		    language='Farsi',
		    slug=product_name,
		    description='description',
		    price=price,
		)
	    product.categories.add(category)

	    return product

    
    def test_unauthenticated_user_adding_product(self):
        product1 = self._create_product_and_category_in_database(
            product_name='product1', 
        )
        
        response = self.client.get(reverse('cart:add', args=[product1.slug],), 
        	follow=True
        )
        session = self.client.session
        
        self.assertEqual(session['cart'][product1.slug], {'price': '100.00'})