from django import template
from django.core.paginator import Paginator
from django.conf import settings
import re

register = template.Library()


@register.inclusion_tag('lecture/_pagenated_lecture_category_list.html')
def show_pagenated_lecture_category_list(request, lecture_category_list):
    print(lecture_category_list)
    paginator = Paginator(lecture_category_list, settings.LECTURE_CATEGORY_NUM_PER_PAGE)
    page = request.GET.get('page')
    pagenated_lecture_category_list = paginator.get_page(page)
    url_with_params = re.sub('(\?|&)page=\d+','',request.get_full_path())
    print(url_with_params)
    if '?' in url_with_params:
        # パラメータがあれば、次につけるパラメータは&page=1などになる。パラメータがなければ?page=1などになる。?か&を付与する
        url_with_params += '&'
    else:
        url_with_params += '?'
    return {'pagenated_lecture_category_list': pagenated_lecture_category_list, 'url_with_params': url_with_params}
