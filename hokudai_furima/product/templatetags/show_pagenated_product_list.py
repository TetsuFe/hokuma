from django import template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from django.urls import reverse
import re

register = template.Library()

@register.inclusion_tag('product/_pagenated_product_list.html')
def show_pagenated_product_list(request, product_list):
    paginator = Paginator(product_list, settings.PRODUCT_NUM_PER_PAGE)
    page = request.GET.get('page')
    paginated_product_list = paginator.get_page(page)
    url_with_params = re.sub('(\?|&)page=\d+','',request.get_full_path())
    print(url_with_params)
    if '?' in url_with_params:
        # パラメータがあれば、次につけるパラメータは&page=1などになる。パラメータがなければ?page=1などになる。?か&を付与する
        url_with_params += '&'
    else:
        url_with_params += '?'
    return {'product_list': paginated_product_list, 'url_with_params': url_with_params}
