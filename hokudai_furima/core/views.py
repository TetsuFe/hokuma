from django.shortcuts import render
from hokudai_furima.product.models import Product
from hokudai_furima.product.utils import get_public_product_list, fetch_latest_sold_timeline


# Create your views here.
def home(request):
    MAX_NUM_LATEST_PRODUCT = 160
    latest_products = get_public_product_list(Product.objects.all().prefetch_related('productimage_set').order_by('-created_date')[:MAX_NUM_LATEST_PRODUCT])
    latest_sold_products = fetch_latest_sold_timeline()
    return render(request, 'home.html', {'product_list': latest_products, 'latest_sold_products': latest_sold_products})
