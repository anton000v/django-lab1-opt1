from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField

class UserOrderForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    wishes = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Order
        exclude = ('status',)

class AdminOrderForm(forms.ModelForm):
    # basket = forms.ChoiceField(
    # widget=forms.Select(attrs={'readonly':'readonly'})
    # )
    # phone_number = forms.CharField(
    # widget=forms.TextInput(attrs={'readonly':'readonly'})
    # )
    # dont_call = forms.CharField(
    # widget=forms.TextInput(attrs={'readonly':'readonly'})
    # )
    class Meta:
        model = Order
        fields = ('status', )
        # exclude = ('phone_number', 'dont_call')
    # def clean_basket(self):
