from django import forms
from website.models import products,locations,user

             

class userForm(forms.ModelForm):
    class Meta:
        model=user
        fields=('username','password','email','name','role')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'role':forms.Select(attrs={'class':'form-control'}),
        }

class productForm(forms.ModelForm):
    class Meta:
        model=products
        fields=('sku','name','description','price','category','serial_item')
        widgets={
            'sku':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'serial_item':forms.Select(attrs={'class':'form-control'}),
        }

class locationForm(forms.ModelForm):
    class Meta:
        model=locations
        fields=('location',)
        widgets={'location':forms.TextInput(attrs={'class':'form-control'})}