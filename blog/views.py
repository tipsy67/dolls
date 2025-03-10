from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from blog.models import BlogArticle
from config.settings import BLOG_PER_PAGE


class BlogListView(ListView):
    model = BlogArticle
    paginate_by = BLOG_PER_PAGE
    template_name = 'dolls/blog.html'
    context_object_name = 'blog_list'
    extra_context = {
    }

    def get_queryset(self):
        return BlogArticle.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    model = BlogArticle
    template_name = 'dolls/blog-post.html'
    context_object_name = 'article'
    extra_context = {
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        # self.streamer_path = self.streamer_path[:3]
        # self.streamer_path.append({'name' : self.object.title[:12]+'...', })
        self.object.save()

        return self.object



def article_like(request):
    post_pk = request.POST.get('pk')
    action = request.POST.get('action')
    if post_pk and action:
        article = BlogArticle.objects.get(pk=post_pk)
        if article:
            if action == 'like':
                article.users_like.add(request.user)
            else:
                article.users_like.remove(request.user)

            return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})


