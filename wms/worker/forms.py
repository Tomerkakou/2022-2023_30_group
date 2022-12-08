from django import forms
from website.models import inventory
class inventoryForm(forms.ModelForm):
    class Meta:
        model=inventory
        fields=('sku','location','amount','serial')
        widgets={
            'sku':forms.Select(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'serial':forms.TextInput(attrs={'class':'form-control'}),
        }