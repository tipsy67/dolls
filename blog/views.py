import json

from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from blog.models import BlogArticle, Comment
from config.settings import BLOG_PER_PAGE
from dolls.src.utils import get_queryset_from_cache
from tags.tag import CheckedTag, ArticleCheckedTag


class BlogListView(ListView):
    model = BlogArticle
    paginate_by = BLOG_PER_PAGE
    template_name = 'dolls/blog.html'
    context_object_name = 'blog_list'
    extra_context = {'tags_list': get_queryset_from_cache('tag_list_article')}

    def get_queryset(self):
        article_list = BlogArticle.objects.filter(is_published=True)
        tags = ArticleCheckedTag(self.request)
        if tags:
            article_list = article_list.filter(tags__pk__in=tags.tags)
        return article_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # last_comment_articles = Comment.objects.order_by('-created_at').distinct('article')[:3]
        # list_popular_articles = BlogArticle.objects.filter(pk__in=last_comment_articles)
        list_popular_articles = BlogArticle.objects.filter(is_published=True, comments__isnull=False).annotate(
            last_comment_date = Max('comments__created_at')).order_by('-last_comment_date')[:3]
        context['list_popular_articles']=list_popular_articles
        return context


class BlogDetailView(DetailView):
    model = BlogArticle
    template_name = 'dolls/blog-single.html'
    context_object_name = 'article'
    extra_context = {}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        # self.streamer_path = self.streamer_path[:3]
        # self.streamer_path.append({'name' : self.object.title[:12]+'...', })
        self.object.save()
        comments = Comment.objects.filter(article=self.object).select_related('parent')
        self.extra_context['comments'] = comments

        return self.object


def article_like(request):
    data = json.loads(request.body)
    post_pk = data.get('pk')
    action = data.get('action')
    if post_pk and action:
        article = BlogArticle.objects.get(pk=post_pk)
        if article:
            if action == 'like':
                article.users_like.add(request.user)
            else:
                article.users_like.remove(request.user)

            return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})


def add_comment_reply(request, parent_id):
    """Добавление ответа на комментарий"""
    if request.method == 'POST':
        parent_comment = Comment.objects.filter(id=parent_id).first()
        article = parent_comment.article
        Comment.objects.create(
            article=article,
            parent=parent_comment,
            owner=request.user,
            text=request.POST['text'],
        )
        return redirect('blog:blog_detail', slug=article.slug)


def add_article_reply(request, article_id):
    """Добавление ответа на комментарий"""
    if request.method == 'POST':
        article = BlogArticle.objects.filter(id=article_id).first()
        Comment.objects.create(
            article=article, owner=request.user, text=request.POST['text']
        )
        return redirect('blog:blog_detail', slug=article.slug)
