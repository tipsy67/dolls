from django.shortcuts import render, redirect

from tags.tag import CheckedTag


def change_tag(request, tag_pk):
    tags = CheckedTag(request)
    tags.change(tag_pk)
    url = request.META.get('HTTP_REFERER') + "#tag_list_id"
    return redirect(url)


def clear_tag(request):
    tags = CheckedTag(request)
    tags.clear()
    url = request.META.get('HTTP_REFERER') + "#tag_list_id"
    return redirect(url)
