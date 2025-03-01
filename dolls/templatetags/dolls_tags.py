from django import template

register = template.Library()


@register.filter
def add_media(url_image):
    if url_image:
        return f'/media/{url_image.image.name}'
    return '#'

@register.filter
def add_attrs(value):
    return value.as_widget(attrs={'class': 'form-control', 'placeholder': f'{value.label} *'})