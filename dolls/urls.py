from django.urls import path

from dolls.apps import DollsConfig
from dolls.views import main_page, product_list_view, product_single_view

app_name = DollsConfig.name

urlpatterns = [
    path('', main_page, name='home'),
    # path('contact/', FeedbackCreateView.as_view(), name='contact'),
    # path('thank-you/', thank_you, name='thank-you'),
    # path('about/', about, name='about'),
    path('shop/', product_list_view, name='shop'),
    path('category/<int:cat>/', product_list_view, name='shop_cat'),
    path('shop-detail/<int:pk>/', product_single_view, name='shop_single'),
]
