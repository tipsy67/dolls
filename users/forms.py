from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ProfileUpdateForm(forms.ModelForm):
    # username = forms.CharField(disabled=True, label="имя пользователя")

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
