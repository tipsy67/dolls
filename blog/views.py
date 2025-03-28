import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from blog.models import BlogArticle, Comment
from config.settings import BLOG_PER_PAGE
from dolls.src.utils import get_queryset_from_cache


class BlogListView(ListView):
    model = BlogArticle
    paginate_by = BLOG_PER_PAGE
    template_name = 'dolls/blog.html'
    context_object_name = 'blog_list'
    extra_context = {
        'tags_list': get_queryset_from_cache('tag_list_article')
    }

    def get_queryset(self):
        return BlogArticle.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogArticle
    template_name = 'dolls/blog-single.html'
    context_object_name = 'article'
    extra_context = {
    }

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
            text=request.POST['text']
        )
        return redirect('blog:blog_detail', slug=article.slug)

def add_article_reply(request, article_id):
    """Добавление ответа на комментарий"""
    if request.method == 'POST':
        article = BlogArticle.objects.filter(id=article_id).first()
        Comment.objects.create(
            article=article,
            owner=request.user,
            text=request.POST['text']
        )
        return redirect('blog:blog_detail', slug=article.slug)