from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dolls.urls', namespace='dolls')),
    path('', include('tags.urls', namespace='tags')),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('cart.urls', 'cart'), namespace='cart')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
