from django import forms
from shop.models import Order


class OrderStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Order.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['status']
