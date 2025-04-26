from django import forms
from pytils.translit import slugify
from django.contrib import admin, messages
from blog.models import BlogArticle, Comment
from blog.tasks import remake_article


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
    actions = ['edit_article']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    @admin.action(description="Преобразовать статью с помощью AI")
    def edit_article(self, request, queryset):
        for article in queryset:
            remake_article.delay(article.pk)
        self.message_user(
            request, f"Не забудьте проконтролировать отредактированный текст!", messages.WARNING
        )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    filter = ['created_at', 'owner']
    search_fields = ['created_at', 'owner']
