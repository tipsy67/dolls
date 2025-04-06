from django.contrib import admin
from django import forms
from django.core.validators import ValidationError
from pytils.translit import slugify

from blog.models import BlogArticle, Comment


class BlogAdminForm(forms.ModelForm):
    slug = forms.CharField(max_length=100, required=False)

    class Meta:
        model = BlogArticle
        fields = '__all__'

    def clean(self, *args, **kwargs):
        if "title" in self.changed_data and "slug" not in self.changed_data:
            self.cleaned_data['slug'] = slugify(self.cleaned_data['title'])
        super().clean(*args, **kwargs)


@admin.register(BlogArticle)
class BlogAdmin(admin.ModelAdmin):
    filter = ['created_at']
    form = BlogAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    filter = ['created_at', 'owner']
    search_fields = ['created_at', 'owner']
