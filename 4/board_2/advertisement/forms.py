from django import forms
from django.core import validators
from .models import Product, Order

# class ProductForm(forms.Form):
#     name = forms.CharField(label='Название' ,max_length=100)
#     price = forms.DecimalField(label="Цена", min_value=1, max_value=100_000, decimal_places=2)
#     description = forms.CharField(
#         label="Описание продукта",
#         widget=forms.Textarea(attrs={"rows": 5, "cols": "20"}),
#         validators=[validators.RegexValidator(
#             regex=r"great",
#             message="Поле должно содержать слово 'great'"
#         )],
#     )
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount"


class OderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"