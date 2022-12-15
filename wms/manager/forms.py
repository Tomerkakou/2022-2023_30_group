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