from django import template

register = template.Library()


@register.filter
def add_media(url_image):
    if url_image:
        return f'/media/{url_image}'
    return '#'
