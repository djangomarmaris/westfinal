from django import forms

from .models import Order
import datetime


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email','city','tc','adress']



