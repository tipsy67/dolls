from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView, article_like

appname = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog-detail/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('like/', article_like, name='like'),
]