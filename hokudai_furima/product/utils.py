from .models import AccessLevelChoice
from .models import Product

def get_public_product_list(product_list):
    return [product for product in product_list if product.access_level == AccessLevelChoice.public.name]


def fetch_latest_sold_timeline():
    latest_sold_products = Product.objects.filter(is_sold=True, sold_date__isnull=False).order_by('-sold_date')[:5]
    product_dict_list = []
    for product in latest_sold_products:
        product_dict_list.append(
            {
                'title': product.title,
                'price': product.price,
                'sold_date': product.sold_date,
                'icon': product.productimage_set.first().thumbnail_100_url,
                'pk': product.pk,
            }
        )
    return product_dict_list
