from django import forms
from website.models import products,locations,user
from django.contrib.auth.models import User,Group

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
    role = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True,)
    """
    set field requierd and email uniqe
    """
    class Meta:
        model=User
        fields=('username','password','email','first_name')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'},required=True),
            'first_name':forms.TextInput(attrs={'class':'form-control'},required=True),
        }
    def save(self):
        try:
            data=self.clean()
            curr=User.objects.create_user(username=data['username'],password=data['password'],first_name=data['first_name'],email=data['email'])
            curr.groups.add(data['role'])
            return curr
        except:
            raise ValueError
        

    

