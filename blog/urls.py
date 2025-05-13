from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import (
    BlogDetailView,
    BlogListView,
    add_article_reply,
    add_comment_reply,
    article_like,
)

appname = BlogConfig.name

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog-detail/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('like/', article_like, name='like'),
    path('comment/reply/<int:parent_id>/', add_comment_reply, name='comment_reply'),
    path('article/reply/<int:article_id>/', add_article_reply, name='article_reply'),
]
