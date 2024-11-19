from django.forms import ModelForm
from .models import Unit, Category, Inventory
from django import forms

class AddProductForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'category', 'unit', 'quantity_in_stock', 'quantity_sold', 'buy_price', 'sell_price', 'stock_alert']

class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class AddUnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['unit']

class UpdateProductForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'quantity_in_stock', 'quantity_sold', 'buy_price', 'sell_price', 'stock_alert']

    category = forms.ModelChoiceField(queryset=Category.objects.all())
    unit = forms.ModelChoiceField(queryset=Unit.objects.all())

    