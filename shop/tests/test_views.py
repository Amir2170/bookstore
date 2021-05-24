from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile


from shop.models import Product, Category, Review


class HomeViewTest(TestCase):

    def test_view_uses_right_template(self):
        response = self.client.get(reverse('shop:home'))
        self.assertTemplateUsed(response, 'shop/home.html')


class DetailViewTest(TestCase):

    def setUp(self):
        image = tempfile.NamedTemporaryFile(suffix='.jpg').name
        category = Category.objects.create(
            name='category',
            slug='category',
            is_sub=False,
        )
        self.product1 = Product.objects.create(
            name='product1',
            author='author',
            language='Farsi',
            slug='product1',
            image=image,
            description='description',
            price=10000,
        )
        self.product2 = Product.objects.create(
            name='product2',
            author='author',
            language='Farsi',
            slug='product2',
            image=image,
            description='description',
            price=10000,
        )
        self.product1.categories.add(category)
        self.product2.categories.add(category)

        self.review1 = Review.objects.create(
            product=self.product1,
            review='my review1',
            )
        self.review2 = Review.objects.create(
            product=self.product2,
            review='my review2',
        )

    def test_detail_view_uses_right_template(self):
        response = self.client.get(reverse('shop:detail', args=(self.product1.id,)))
        self.assertTemplateUsed(response, 'shop/detail.html')

    def test_detail_view_sends_correct_product_to_the_template(self):
        response = self.client.get(reverse('shop:detail', args=(self.product1.id,)))
        self.assertContains(response, 'product1')
        self.assertNotContains(response, 'product2')
        self.assertContains(response, 'category')

    def test_detail_view_sends_the_correct_review_if_it_exists(self):
        response = self.client.get(reverse('shop:detail', args=(self.product1.id,)))
        self.assertContains(response, 'my review1')
        self.assertNotContains(response, 'my review2')


class CategoryViewTest(TestCase):
    def setUp(self):
        image = tempfile.NamedTemporaryFile(suffix='.jpg').name
        self.main_category = Category.objects.create(
            name='main_category',
            slug='main_category',
            is_sub=False,
        )
        self.sub_category = Category.objects.create(
            name='sub_category',
            slug='sub_category',
            is_sub=True,
            category=self.main_category
        )
        self.product = Product.objects.create(
            name='product',
            author='author',
            language='Farsi',
            slug='product1',
            image=image,
            description='description',
            price=10000,
        )
        self.product.categories.add(self.main_category, 
            self.sub_category
        )

    def test_view_sub_category_and_main_category(self):
        response = self.client.get(reverse('shop:category', args=(self.main_category.slug,)))
        self.assertContains(response, 'main_category')
        self.assertContains(response, 'sub_category')
        self.assertContains(response, 'product')

    def test_view_sub_category(self):
        response = self.client.get(reverse('shop:category', args=(self.sub_category.slug,)))
        self.assertContains(response, 'sub_category')
        self.assertContains(response, 'product')
        self.assertNotContains(response, 'main_category')
  
  
  
class TestDownloadView(TestCase):
    
    def setUp(self):
        pdf = SimpleUploadedFile(
            "file.pdf", b"Hello world",
            content_type="application/pdf",
        )
        category = Category.objects.create(
            name='category',
            slug='category',
            is_sub=False,
        )
        self.product1 = Product.objects.create(
            name='product1',
            author='author',
            language='Farsi',
            slug='product1',
            description='description',
            price=10000,
            upload=pdf
        )
        
    
    def test_download_view_downloads_a_file(self):
        response = self.client.get(
            reverse('shop:download', 
            args = [self.product1.slug]),
            HTTP_REFERER='http://localhost:8000/cart/detail',
        )
        
        self.assertEqual(
            response.get('Content-Disposition'),
            'attachment; filename="product1.pdf"'
        )