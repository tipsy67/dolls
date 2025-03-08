from django.shortcuts import get_object_or_404
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

def add_like(request, pk):
    instance = get_object_or_404(BlogArticle, pk=pk)
    if instance:
        instance.like_counter += 1
        instance.save()

    return None
