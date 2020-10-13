from django import forms
from .models import UserRating

class UserRatingForm(forms.Form):
    RATING_CHOICES = (
        ('good', '良い'),
        ('normal', '普通'),
        ('bad', '悪い'),
    )
    rating = forms.ChoiceField(label='評価', widget=forms.RadioSelect, choices=RATING_CHOICES)
