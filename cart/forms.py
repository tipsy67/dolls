from django import forms

from cart.models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'country',
            'postal_code',
            'address',
            'comment',
        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if in
