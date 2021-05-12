from django.contrib.auth import get_user_model
from django.test import Client

from shop.models import Product, Category 

User = get_user_model()


def _create_product_and_category_in_database(product_name,
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