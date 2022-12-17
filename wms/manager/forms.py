from django import forms
from website.models import products,locations,user1
from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm

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
             

class userForm(forms.ModelForm):
    class Meta:
        model=user1
        fields=('username','password','email','full_name','role')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'full_name':forms.TextInput(attrs={'class':'form-control'}),
            'role':forms.Select(attrs={'class':'form-control'})
        }
    def save(self):
        data=self.clean()
        user=user1.objects.create_user(username=data['username'],password=data['password'],full_name=data['full_name'],email=data['email'],role=data['role'])
        user.set_password(data['password'])
  
        

    

