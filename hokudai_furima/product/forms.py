from django import forms

from .models import Product, ProductImage, Category
from hokudai_furima.lecture.models import LectureCategory


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'category', 'lecture_category', 'access_level')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['placeholder'] = '商品の状態（未使用、傷あり等）、その他詳しい説明など'
        self.fields['title'].widget.attrs['placeholder'] = '（例）入門線形代数'
        self.fields['category'].label = 'カテゴリ'
        self.fields['lecture_category'].label = '科目区分'

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='その他')
    lecture_category = forms.ModelChoiceField(queryset=LectureCategory.objects.filter(children__isnull=True))


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def __init__(self, i, *args, **kwargs):
        super(ProductImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()
        self.fields['image'].widget.attrs={'name':'image'+str(i), 'style':'display:none;', 'id':'file_'+str(i) , 'onchange': 'fileget(this,\''+str(i)+'\');', }

    @property
    def thumbnail_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['600x600'].url
