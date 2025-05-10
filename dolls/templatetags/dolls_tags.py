from django import template

register = template.Library()


@register.filter
def add_media(url_image):
    if url_image:
        return f'/media/{url_image.image.name}'
    return '#'


@register.filter
def add_media_insta(image):
    if image:
        return f'/media/{image.name}'
    return '#'


@register.filter
def add_attrs(value):
    return value.as_widget(
        attrs={'class': 'form-control'}
        # attrs = {'class': 'form-control', 'placeholder': f'{value.label} *'}
    )


@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


@register.simple_tag
def percent(total_cost, limit):
    try:
        limit = int(limit)
    except (ValueError, TypeError):
        limit = 0

    return round((total_cost / limit) * 100)
