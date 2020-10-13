from django import template

register = template.Library()

@register.inclusion_tag('matching_offer/_matching_offer_list.html')
def show_matching_offer_list(matching_offer_list):
    return {'matching_offer_list': matching_offer_list}
