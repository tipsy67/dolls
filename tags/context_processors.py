from tags.tag import ArticleCheckedTag, ProductCheckedTag


def tags(request):
    return {
        'tags_article': ArticleCheckedTag(request),
        'tags_product': ProductCheckedTag(request),
    }
