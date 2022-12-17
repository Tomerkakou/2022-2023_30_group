from django import forms
from website.models import user1
from django.contrib.auth.forms import PasswordChangeForm

class user_updateForm(forms.ModelForm):
    class Meta:
        model=user1
        fields=('username','email','full_name')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
        }

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user,*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    