import os

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from dolls.models import Category, Product, Image
from pytils.translit import slugify

from dolls.tasks import remake_description


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.action(description="Опубликовать выбранные записи")
def set_published(self, request, queryset):
    count = queryset.update(is_published=True)
    self.message_user(request, f"Изменено {count} записей.")

@admin.action(description="Снять с публикации выбранные записи")
def set_draft(self, request, queryset):
    count = queryset.update(is_published=False)
    self.message_user(
        request, f"{count} записей сняты с публикации!", messages.WARNING
    )

@admin.action(description="Преобразовать описание с помощью AI")
def edit_description(self, request, queryset):
    for product in queryset:
        remake_description.delay(product.pk)
    self.message_user(
        request, f"Не забудьте проконтролировать отредактированный текст!", messages.WARNING
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'price',
        'old_price',
        'quantity',
        'photo_product',
        'is_published',
    )
    inlines = [ImageInline]
    list_display_links = ('name',)
    actions = [set_draft, set_published, edit_description]

    @admin.display(description="Просмотр")
    def photo_product(self, product: Product):
        if product.one_image:
            return mark_safe(f"<img src='{product.one_image.image.url}' width=50>")
        return "Без изображения"

    def save_formset(self, request, form, formset, change):
        product_name = form.cleaned_data.get('name', '')
        for inline_form in formset.forms:
            image_name = inline_form.cleaned_data.get('name', '')
            if inline_form.cleaned_data and (
                image_name is None or len(image_name) == 0
            ):
                file_path = inline_form.cleaned_data.get('image', '')
                file_name = os.path.basename(file_path.name)
                inline_form.instance.name = f"{slugify(product_name)}-{file_name}"
        super().save_formset(request, form, formset, change)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

    # def save_model(self, request, obj, form, change):
    #     if not self.pk:
    #         self.slug = slugify(self.title)
    #     super().save_model(request, obj, form, change)
