from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum

from bookstore_project import settings


class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		null=True, blank=True
	)
	creation_date = models.DateTimeField(verbose_name=_('creation date'))
	checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
	products = models.ManyToManyField("shop.Product", blank=True)

	class Meta:
		verbose_name = _('cart')
		verbose_name_plural = _('carts')
		ordering = ('-creation_date',)

	def __str__(self):
		return str(self.creation_date)

	@property
	def total_price(self):
		tp_dict = Cart.objects.aggregate(
			tp=Sum('products__price')
		)
		return tp_dict['tp']

