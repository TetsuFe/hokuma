from django import template

register = template.Library()


@register.inclusion_tag('matching_offer/_details_images_carousel.html')
def details_images_carousel(details_images):
    return {'images': details_images}
