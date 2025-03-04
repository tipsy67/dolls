from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from users.models import Address


class CustomLoginForm(AuthenticationForm):
    pass

class ProfileUpdateForm(forms.ModelForm):
    # username = forms.CharField(disabled=True, label="имя пользователя")
    # address = forms.ModelChoiceField(
    #     queryset=None,
    #     initial=None,
    #     label="Адрес",
    #     empty_label="Адрес не выбран"
    # )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self.fields.get('username')
        username.disabled = True
        username.label = "Логин"
        email = self.fields.get('email')
        email.label = "Почта"

        # current_user = kwargs.get('instance')
        # current_queryset = Address.objects.filter(user=current_user)
        # self.fields['address'].queryset = current_queryset
        # if current_queryset:
        #     self.fields['address'].initial = getattr(current_queryset.filter(is_active=True).first(), 'id')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'phone',
            'avatar',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        username = self.fields.get('username')
        username.label = "Логин"
        email = self.fields.get('email')
        email.label = "Почта"
        email.required = True
        first_name = self.fields.get('first_name')
        first_name.required = True
        last_name = self.fields.get('last_name')
        last_name.required = True

class AddressForm (forms.ModelForm):

    class Meta:
        model = Address
        exclude = ('is_active', 'user')

