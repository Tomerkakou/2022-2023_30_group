from django import forms
from website.models import products

class productChoose(forms.Form):
    product = forms.ModelChoiceField(queryset=products.objects.all(),
                                    empty_label="---------",widget=forms.Select(),label='')