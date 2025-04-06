from django.contrib import admin

from users.models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    show_change_link = True
    fields = ('name', 'is_active')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username')
    list_display_links = ('username',)
    inlines = [AddressInline]

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_display_links = ('name',)
