from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    LoginView,
    ProfileUpdateView,
    UserCreateView,
    confirm_user,
    logout_form,
)

appname = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-form/', logout_form, name='logout_form'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('create-user/', UserCreateView.as_view(), name='create_user'),
    path('confirm/<str:token>', confirm_user, name='confirm'),
]
