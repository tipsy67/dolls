from django.contrib import admin
from django.template.loader import render_to_string

from dolls.tasks import sendmail
from subscribes.models import Article, Recipients
from subscribes.src.utils import get_recipients
from tunes.src.utils import get_value_from_tunes


@admin.register(Recipients)
class RecipientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('is_test', 'title', 'updated_at')
    actions = ('send_email',)
    list_display_links = ('title',)

    @admin.action(description='Разослать')
    def send_email(self, request, queryset):
        list_recipients = get_recipients()
        only_author = [get_value_from_tunes('author_email')]
        list_recipients.extend(only_author)
        count = len(queryset)

        for article in queryset:
            if article.is_test:
                sendmail.delay(
                    only_author,
                    article.title,
                    render_to_string('subscribes/article.html', {'article': article}),
                )
            else:
                sendmail.delay(
                    list_recipients,
                    article.title,
                    render_to_string('subscribes/article.html', {'article': article}),
                )

        self.message_user(request, f"Разослано {count}.")
