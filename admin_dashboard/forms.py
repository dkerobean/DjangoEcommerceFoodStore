from django.forms import ModelForm
from frontend.models import Product


class AddProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            
        self.fields['category'].widget.attrs.update(
            {'id': 'Categories', 'class': 'form-select'})
