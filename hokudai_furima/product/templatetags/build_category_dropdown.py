from django import template
from hokudai_furima.product.models import Category

register = template.Library()


@register.inclusion_tag('product/_category_list_nav.html')
def build_category_dropdown():
    category_root_nodes = Category.objects.filter(parent=None)
    return {'category_root_nodes': category_root_nodes}
