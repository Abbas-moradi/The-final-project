from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Specifications', {'fields':('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields':('email', 'phone_number', 'full_name', 'password1', 'password2')}),
    )

    search_fields = ('email', 'phone_number', 'full_name')   # Search based on specified values
    ordering = ('full_name',)   # ordering by specified values
    filter_horizontal = ()   # Display two values side by side when using permissions


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

# After finishing the settings, go to the setting section and add the following command
# AUTH_USER_MODEL = 'accounts.User'