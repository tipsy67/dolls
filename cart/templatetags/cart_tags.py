from django import template

register = template.Library()


@register.filter
def add_media(url_image):
    if url_image:
        return f'/media/{url_image}'
    return '#'

@register.filter
def get_value_from_dict(obj_dict, key):
    return obj_dict.get(key, "error get_value_from_dict")