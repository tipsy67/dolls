from django.urls import path

from dolls.apps import DollsConfig
from dolls.views import (
    main_page,
    product_list_view,
    product_single_view,
    product_preview_update,
    about,
    history, privacy_policy, shipping, user_agreement, FeedbackCreateView, thank_you, product_filter_view,
)

app_name = DollsConfig.name

urlpatterns = [
    path('', main_page, name='home'),
    # path('contact/', FeedbackCreateView.as_view(), name='contact'),
    # path('thank-you/', thank_you, name='thank-you'),
    path('about/', about, name='about'),
    path('history/', history, name='history'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('shipping/', shipping, name='shipping'),
    path('user-agreement/', user_agreement, name='user_agreement'),
    path('thank-you/', thank_you, name='thank_you'),
    path('contact-us/', FeedbackCreateView.as_view(), name='contact_us'),
    path('shop/', product_list_view, name='shop'),
    path('ajax/shop-filter/', product_filter_view, name='shop_filter'),
    path('category/<int:cat>/', product_list_view, name='shop_cat'),
    path('shop-detail/<int:pk>/', product_single_view, name='shop_single'),
    path(
        "ajax/product-preview/<int:pk>/",
        product_preview_update,
        name="product_preview_update",
    ),
]
