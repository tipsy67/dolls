from django.contrib import admin
from django.utils.safestring import mark_safe

from tunes.models import Banner, Feedback, TunesDict


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'email', 'phone', 'is_read')


@admin.register(TunesDict)
class TunesDictAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'photo_banner', 'title')

    @admin.display(description="Просмотр")
    def photo_banner(self, banner: Banner):
        if banner.image:
            return mark_safe(f"<img src='{banner.image.url}' width=50>")
        return "Без изображения"
