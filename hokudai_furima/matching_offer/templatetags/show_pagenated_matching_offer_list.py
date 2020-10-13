from django import template
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
import re

register = template.Library()

@register.inclusion_tag('matching_offer/_pagenated_matching_offer_list.html')
def show_pagenated_matching_offer_list(request, matching_offer_list):
    paginator = Paginator(matching_offer_list, settings.MATCHING_OFFER_NUM_PER_PAGE)
    page = request.GET.get('page')
    paginated_matching_offer_list = paginator.get_page(page)
    url_with_params = re.sub('(\?|&)page=\d+','',request.get_full_path())
    if '?' in url_with_params:
        # パラメータがあれば、次につけるパラメータは&page=1などになる。パラメータがなければ?page=1などになる。?か&を付与する
        url_with_params += '&'
    else:
        url_with_params += '?'
    return {'matching_offer_list': paginated_matching_offer_list, 'url_with_params': url_with_params}
