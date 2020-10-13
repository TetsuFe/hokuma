from django import forms

class SearchProductKeywordForm(forms.Form):
    q = forms.CharField(label="検索ワード")

class SearchProductOptionForm(forms.Form):
    PRICE_RANGE_OPTIONS = (('0_1000000', '全て'), ('0_1000','0 ~ 1000'), ('1000_3000', '1000 ~ 3000'), ('3000_5000', '3000 ~ 5000'), ('5000_10000', '5000 ~ 10000'), ('10000_1000000', '10000 ~ '))
    IS_SOLD_OPTIONS = (('all', '全て'), ('sold_out', '売り切れ'), ('not_sold', '販売中'))
    SORT_METHOD_OPTIONS = (('sort_new', '出品日が新しい順'), ('sort_old', '出品日が古い順'), ('sort_low', '価格が安い順'), ('sort_high', '価格が高い順'))
    price_range = forms.ChoiceField(label="価格帯", choices=PRICE_RANGE_OPTIONS)
    is_sold = forms.ChoiceField(label="販売中/売り切れ", choices=IS_SOLD_OPTIONS)
    sort_method = forms.ChoiceField(label="並び替え", choices=SORT_METHOD_OPTIONS)

