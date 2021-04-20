from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm 
from .models import CustomUser


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'name', 'is_admin',)
	list_filter = ('is_admin',)

	fieldsets = (
		(None, {'fields': ('email', 'password',)}),
		('Personal info', {'fields': ('name', 'phone',)}),
		('Permission', {'fields': ('is_admin', 'is_active',)}),
		)

	add_fieldsets = (
		(None,{
			'fields': (
				'email', 'phone','name', 
				'password1', 'password2'
			)
		}
	),
)

	search_fields = ('email', 'name',)
	ordering = ('email',)
	filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)

admin.site.unregister(Group)