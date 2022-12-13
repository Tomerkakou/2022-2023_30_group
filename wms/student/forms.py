from django import forms
from website.models import orders
class productForm(forms.ModelForm):
    class Meta:
        model=orders
        fields=('sku','name','descprition','price','category','serial_item')
        widgets={
            'sku':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'descprition':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'serial_item':forms.Select(attrs={'class':'form-control'}),
        }