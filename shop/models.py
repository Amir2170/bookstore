from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models
from bookstore_project import settings


class Category(models.Model):
	category = models.ForeignKey(
		'self', on_delete=models.CASCADE,
		null=True, blank=True,
		related_name='s_category',
	)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	is_sub = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)
		verbose_name_plural = 'categories'


class Product(models.Model):
	BOOK_LANGUAGE = (
		('Fa', 'Farsi'),
		('En', 'English'),
	)
	categories = models.ManyToManyField(Category)
	name = models.CharField(max_length=300)
	slug = models.SlugField(max_length=300, unique=True)
	image = models.ImageField(upload_to='shop/%Y/%m/%d/')
	description = models.TextField()
	price = models.IntegerField()
	language = models.CharField(max_length=10, 
		choices=BOOK_LANGUAGE, default='Farsi'
	)
	author = models.CharField(max_length=100, 
		default=None, null=True
	)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, null=True, blank=True,
	)
	review = models.TextField()