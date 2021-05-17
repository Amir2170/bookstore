from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from cart.models import Cart
from shop.models import Product, Category
from .functions import(
     _create_product_and_category_in_database,
)

User = get_user_model()



class TestAddView(TestCase):
    
    def _create_user_model_and_login(self, email='testuser1@gmail.com', 
        password='testuser1'):
        user = User.objects.create_user(email=email,
            phone='+989211333333',
            name='amir',
            password=password,
        )
        self.client.login(email='testuser1@gmail.com', 
            password='testuser1'
        )
        return user	 	 
    
    
    def test_unauthenticated_user_adding_product(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        response = self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )
        session = self.client.session
        
        self.assertEqual(session['cart'][product1.slug], 
            {'price': '100.00'}
        )
        self.assertNotContains(response, "Already added")
         
    
    def test_unauthenticated_user_adding_product_twice(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
     
        self.client.post(reverse('cart:add', args=[product1.slug],))
        response = self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True)
        
        self.assertRedirects(response, reverse('shop:home'))
        self.assertContains(response, "Already added")
  
    
    def test_authenticated_user_adding_product(self):
        self._create_user_model_and_login()
        
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        response = self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )

        cart = Cart.objects.first()
        
        session = self.client.session
        
        self.assertEqual(cart.products.first(), product1)

   
    def test_authenticated_user_adding_product_twice(self):
        self._create_user_model_and_login()
        
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        self.client.post(reverse('cart:add', 
            args=[product1.slug],))
        
        response = self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True)
        
        self.assertRedirects(response, reverse('shop:home'))
        self.assertContains(response, "Already added")
    
    
    def test_view_redirects_to_home_page_upon_successfully_adding_product(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        response = self.client.post(reverse('cart:add', 
            args=[product1.slug],))
        
        self.assertRedirects(response, reverse('shop:home'))
    
    
    def test_view_shows_right_message_after_successfully_adding_product(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        response = self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True)
        
        self.assertContains(response, "Product added successfully")
        
        
        
class DetailViewTest(TestCase):
    
    def _create_user_model_and_login(self, email='testuser1@gmail.com', 
        password='testuser1'):
        user = User.objects.create_user(email=email,
            phone='+989211333333',
            name='amir',
            password=password,
        )
        self.client.login(email='testuser1@gmail.com', 
            password='testuser1'
        )
        return user	 	 
    
    def test_detail_view_uses_right_template(self):
        response = self.client.get(reverse('cart:detail'))
        self.assertTemplateUsed(response, 'detail.html')
    
    
    def test_authenticated_user_attempts_to_view_an_empty_cart(self):
        self._create_user_model_and_login()
        
        response = self.client.get(reverse('cart:detail'))
        
        self.assertEqual(response.context['cart'], {})    
    
    
    def test_unauthenticated_user_attempts_to_view_an_empty_cart(self):
        response = self.client.get(reverse('cart:detail'))
        
        self.assertEqual(response.context['cart'], {}) 
        
    
    def test_authenticated_users_attempts_to_view_their_cart(self):
        user = self._create_user_model_and_login()
            
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )
        cart = Cart.objects.first()
        
        response = self.client.get(reverse('cart:detail'))
        
        self.assertEqual(response.context['cart'], cart)
        
     
    # bookstore uses sessions for unauthenticated users so in this 
    # test i test context of the response against an expected dict
    # for cart session object    
    def test_unauthenticated_users_attempts_to_view_their_cart(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )
        
        self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )
        
        response = self.client.get(reverse('cart:detail'))
        
        self.assertEqual(response.context['cart'], 
            {'product1': {'price': '100.00'}}
        )

    

class RemoveView(TestCase):
    
    def _create_user_model_and_login(self, email='testuser1@gmail.com', 
        password='testuser1'):
        user = User.objects.create_user(email=email,
            phone='+989211333333',
            name='amir',
            password=password,
        )
        self.client.login(email='testuser1@gmail.com', 
            password='testuser1'
        )
        return user	 	 
    
    
    def test_authenticated_user_removing_a_product_and_redirects_to_home(self):
        self._create_user_model_and_login()
        
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )    
        self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )
        cart = Cart.objects.first()
        
        self.assertTrue(
            cart.products.filter(name='product1').exists()
        )
        
        response = self.client.get(reverse('cart:remove',
            args=[product1.slug],)
        )
        
        self.assertFalse(
            cart.products.filter(name='product1').exists()
        )
        self.assertRedirects(response, reverse('shop:home'))
    
    
    def test_unauthenticated_user_removing_a_product_and_redirects_to_home(self):
        product1 = _create_product_and_category_in_database(
            product_name='product1', 
        )    
        self.client.post(reverse('cart:add', 
            args=[product1.slug],), follow=True,
        )
        session = self.client.session
        
        self.assertTrue(product1.slug in session['cart'])
        
        response = self.client.get(reverse('cart:remove', 
            args=[product1.slug],)
        )
        session = self.client.session
        
        self.assertFalse(product1.slug in session['cart'])
        self.assertRedirects(response, reverse('shop:home'))