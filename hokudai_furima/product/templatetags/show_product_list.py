from django import template

register = template.Library()

@register.inclusion_tag('product/_product_list.html')
def show_product_list(product_list):
    return {'product_list': product_list}
