from django.contrib import admin

from tunes.models import Feedback, TunesDict, Banner, Contact


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'address',)

@admin.register(TunesDict)
class TunesDictAdmin(admin.ModelAdmin):
    list_display = ('key', 'value_int', 'value_char', 'value_date', 'value_time')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_content')
