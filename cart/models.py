from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum

from bookstore_project import settings


class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		null=True, blank=True
	)
	creation_date = models.DateTimeField(verbose_name=_('creation date'))
	checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))

	class Meta:
		verbose_name = _('cart')
		verbose_name_plural = _('carts')
		ordering = ('-creation_date',)

	def __str__(self):
		return self.creation_date

	@property
	def total_price(self):
		tp_dict = Cart.objects.aggregate(
			tp=Sum('item__unit_price')
		)
		return tp_dict['tp']


class Item(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('cart'))
	unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name=_('unit price'))
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	class Meta:
		verbose_name = _('item')
		verbose_name_plural = _('items')
		ordering = ('cart',)


	def __str__(self):
		return _(f"{self.product.__class__.__name__}")

	@property
	def product(self):
		return self.content_type.get_object_for_this_type(pk=self.object_id)

	@product.setter
	def product(self, product):
		self.content_type = ContentType.objects.get_for_model(type(product))
		self.object_id = product.id

