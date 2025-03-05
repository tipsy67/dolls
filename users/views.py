import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from users.forms import CreateUserForm, ProfileUpdateForm, AddressForm
from users.models import User, Address


class LoginView(BaseLoginView):
    template_name = 'dolls/user-form.html'
    extra_context = {'title_form': 'Вход на сайт'}

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'recovery' in form.data:
            username = form.data.get('username')
            user = User.objects.filter(username=username).first()
            if user is not None:
                password = user.generate_password(8)
                user.password = make_password(password)
                user.save()
                # sendmail.delay(
                #     [user.email],
                #     'Восстановление пароля',
                #     f'{user.username} Ваш новый пароль {password}',
                # )
                messages.success(self.request, 'На вашу почту отправлен пароль')
                return redirect(reverse('users:login'))
            else:
                messages.warning(self.request, f'Пользователя {username} не существует')
        return super().form_invalid(form)


class ProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = 'dolls/user-form.html'
    extra_context = {'title_form': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = CreateUserForm
    template_name = 'dolls/user-form.html'
    extra_context = {'title_form': 'Регистрация пользователя', 'create_user': True}
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        token = secrets.token_hex(16)
        user.is_active = False
        user.token = token
        user.save()
        # sendmail.delay(
        #     [user.email],
        #     'Подтверждение регистрации',
        #     'Пожалуйста подтвердите свой адрес электронной почты для завершения регистрации\n'
        #     + f'http://{self.request.get_host()}/confirm/{token}',
        # )
        print(f'http://{self.request.get_host()}/confirm/{token}')
        messages.success(self.request, 'Проверьте почту и подтвердите свой адрес')

        return super().form_valid(form)


def confirm_user(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    return redirect(reverse('users:login'))


def logout_form(request):
    context = {
        'title_form': 'Вы действительно хотите выйти?',
        'return_url': request.META.get('HTTP_REFERER'),
    }

    return render(request, 'dolls/user-logout.html', context)


# Адреса


class AddressCreateView(CreateView):
    model = Address
    template_name = 'dolls/address-form.html'
    form_class = AddressForm
    extra_context = {'title_form': "Новый адрес доставки"}

    def get_success_url(self):
        return self.request.GET.get('next', self.request.POST.get('next', '/'))

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()

        return super().form_valid(form)


class AddressUpdateView(UpdateView):
    model = Address
    template_name = 'dolls/address-form.html'
    form_class = AddressForm
    extra_context = {'title_form': "Адрес доставки"}

    def get_success_url(self):
        return self.request.GET.get('next', self.request.POST.get('next', '/'))


class AddressDeleteView(DeleteView):
    model = Address
    template_name = 'dolls/address-delete.html'
    extra_context = {
        'title_form': "Вы действительно хотите удалить этот адрес?",
        # 'back_url': reverse_lazy(request.GET.get('next', '/'))
    }

    def get_success_url(self):
        return self.request.GET.get('next', self.request.POST.get('next', '/'))


def change_status(request, pk):
    Address.objects.filter(user=request.user).update(is_active=False)
    address = get_object_or_404(Address, pk=pk)
    address.is_active = True
    address.save()

    url = request.META.get('HTTP_REFERER')
    return redirect(url)


# /Адреса
