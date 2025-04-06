from django.shortcuts import render, redirect

from tags.tag import CheckedTag, ArticleCheckedTag, ProductCheckedTag


def change_tag(request, tag_pk):
    model = request.GET.get('model')
    if model == 'Article':
        tags = ArticleCheckedTag(request)
    else:
        tags = ProductCheckedTag(request)

    tags.change(tag_pk)
    url = request.META.get('HTTP_REFERER')
    return redirect(url)


def clear_tag(request):
    model = request.GET.get('model')
    if model == 'Article':
        tags = ArticleCheckedTag(request)
    else:
        tags = ProductCheckedTag(request)
    tags.clear()
    url = request.META.get('HTTP_REFERER') + "#tag_list_id"
    return redirect(url)
