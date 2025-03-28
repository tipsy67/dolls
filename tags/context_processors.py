from tags.tag import CheckedTag, ArticleCheckedTag, ProductCheckedTag


def tags(request):
    return {'tags_article': ArticleCheckedTag(request), 'tags_product': ProductCheckedTag(request)}
