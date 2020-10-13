from django import forms
from .models import MatchingOfferTalk
from .models import MatchingOffer, MatchingOfferImage


class MatchingOfferTalkForm(forms.ModelForm):
    class Meta:
        model = MatchingOfferTalk
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)


class MatchingOfferForm(forms.ModelForm):

    class Meta:
        model = MatchingOffer
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs):
        super(MatchingOfferForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'タイトル'
        self.fields['description'].label = '説明'
        self.fields['title'].widget.attrs['placeholder'] = '（例）プログラミングの勉強を一緒にやってくれる友達募集！'
        self.fields['description'].widget.attrs['placeholder'] = '開催場所・時間（毎週何時など）・内容・連絡先などをお書きください'


class MatchingOfferImageForm(forms.ModelForm):
    class Meta:
        model = MatchingOfferImage
        fields = ('image',)

    def __init__(self, i, *args, **kwargs):
        super(MatchingOfferImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = forms.FileInput()
        self.fields['image'].widget.attrs={'name':'image'+str(i), 'style':'display:none;', 'id':'file_'+str(i) , 'onchange': 'fileget(this,\''+str(i)+'\');', }

    @property
    def thumbnail_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.thumbnail['600x600'].url
