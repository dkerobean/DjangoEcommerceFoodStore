from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Address
from django import forms


class UserRegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields=['username','email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input',
                 'placeholder': field.label})
            
            
class UserProfileEditForm(ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['email']
        
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=30, required=True)
        
    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input',
                 'placeholder': field.label})
            
            
class UserAddressEditForm(MoelForm):
    
    class Meta:
        model = Address
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input',
                 'placeholder': field.label})
        
    
    