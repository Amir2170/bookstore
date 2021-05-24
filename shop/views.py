from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.messages import get_messages
from django.http import HttpResponse, Http404
from django.http import FileResponse
import os

from .models import Category, Product, Review
from bookstore_project import settings


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/home.html', {
        'categories': categories, 'products': products
    }
)


def detail(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'shop/detail.html', {
        'categories': categories, 'product': product,
        'reviews': reviews,
        }
    )


def category(request, slug):
    main_category = get_object_or_404(Category, slug=slug)
    sub_categories = Category.objects.filter(category=main_category)
    products = Product.objects.filter(categories=main_category)
    return render(request, 'shop/category_detail.html',{
        'main_category': main_category, 
        'sub_categories': sub_categories,
        'products': products,
        }
    )


def download(request, slug):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        raise Http404
    
    product = Product.objects.get(slug=slug)
    
    return FileResponse(
        open(product.upload.path, 'rb'),
        as_attachment=True, 
        filename= product.name + '.pdf'
    )