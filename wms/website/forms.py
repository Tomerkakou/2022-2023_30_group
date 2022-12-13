from django import forms
from website.models import user

class user_updateForm(forms.ModelForm):
    class Meta:
        model=user
        fields=('username','password','email','name')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
        }