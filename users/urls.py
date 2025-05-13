from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    AddressCreateView,
    AddressDeleteView,
    AddressUpdateView,
    LoginView,
    ProfileUpdateView,
    UserCreateView,
    change_status,
    confirm_user,
    logout_form,
)

appname = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-form/', logout_form, name='logout_form'),
    path('user-create/', UserCreateView.as_view(), name='create_user'),
    path('user-update/', ProfileUpdateView.as_view(), name='profile'),
    # path('user-update/', ProfileUpdateView.as_view(), name='profile'),
    path('confirm/<str:token>/', confirm_user, name='confirm'),
    path('address-create/', AddressCreateView.as_view(), name='address_create'),
    path(
        'address-update/<int:pk>/', AddressUpdateView.as_view(), name='address_update'
    ),
    path(
        'address-delete/<int:pk>/', AddressDeleteView.as_view(), name='address_delete'
    ),
    path('address-status/<int:pk>/', change_status, name='change_status'),
]
