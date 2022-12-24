from django import forms
from website.models import inventory,locations
class inventoryForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=locations.objects.exclude(location='RETRNS'),
                                    to_field_name = 'location',
                                    empty_label="---------",widget=forms.Select(attrs={'class':'form-control'}),required=True)
    class Meta:
        model=inventory
        fields=('sku','location','amount','serial')
        widgets={
            'sku':forms.Select(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            'serial':forms.TextInput(attrs={'class':'form-control'}),
        }