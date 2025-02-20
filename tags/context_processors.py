from tags.tag import CheckedTag


def tags(request):
    return {'tags': CheckedTag(request)}
