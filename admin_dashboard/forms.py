from django.forms import ModelForm
from frontend.models import Product
from django import forms
from frontend.models import Category, Tag


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        self.fields['category'].queryset = Category.objects.all()

        self.fields['tag'].widget = forms.CheckboxSelectMultiple()
        self.fields['tag'].queryset = Tag.objects.all()

        self.fields['category'].widget.attrs.update(
            {'class': 'form-check form-check-inline',
             'type': 'checkbox'}),

        self.fields['tag'].widget.attrs.update(
            {'class': 'form-check form-check-inline mb-3',
             'type': 'checkbox'}),

        # self.fields['product_picture'].widget.attrs.update(
        #     {'class': 'ec-image-upload', 'id': 'imageUpload',
        #     'type': 'file'})


class EditCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EditCategoryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
