from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Product, Address

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)
    password2 = forms.CharField(label="Confirm Password (again)", widget=forms.PasswordInput)

    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email'] 
        labels = {'email': 'Email'}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity', 'category']
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'price': 'Price',
            'stock_quantity': 'Stock Quantity',
            'category': 'Category',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'zip_code', 'country']
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'ZIP Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }



