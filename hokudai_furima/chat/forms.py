from django import forms

from .models import Talk

class TalkForm(forms.ModelForm):

    class Meta:
        model = Talk
        fields = ('sentence',)

    def __init__(self, *args, **kwargs): 
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        #self.labels['sentence'].widget.attrs.update({'style': 'display: none;'})
        #self.fields['sentence'].widget.attrs.update({'class=hidden_label')
        #self.fields['sentence'].label = ''
