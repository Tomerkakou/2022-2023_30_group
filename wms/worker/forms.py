from django import forms
from website.models import inventory,locations,products

class inventoryForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=locations.objects.exclude(location='RETRNS'),
                                    to_field_name = 'location',
                                    empty_label="---------",widget=forms.Select(attrs={'class':'form-control'}),required=True)
    sku = forms.ModelChoiceField(queryset=products.objects.all().order_by('category','sku'),
                                    to_field_name = 'sku',
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

class locationform(forms.Form):
    location = forms.ModelChoiceField(queryset=locations.objects.exclude(location='RETRNS'),
                                    empty_label="---------",widget=forms.Select(),label='')

        
        