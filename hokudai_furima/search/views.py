from django.shortcuts import render
from hokudai_furima.product.models import Product
from .forms import SearchProductKeywordForm, SearchProductOptionForm
from django.http import JsonResponse
from hokudai_furima.product.utils import get_public_product_list
import re


def search_product(request):
    if request.method == "GET":
        keyword_form = SearchProductKeywordForm(request.GET)
        option_form = SearchProductOptionForm(request.GET)
        if keyword_form.is_valid() and option_form.is_valid():
            search_results = get_public_product_list(search(request))
            if len(search_results) > 0:
                return render(request,
                              'search/product/search_product.html',
                              {'product_list': search_results, 'keyword_form': keyword_form,
                               'option_form': option_form, 'is_searched': True})
            else:
                latest_products = get_public_product_list(Product.objects.all().order_by('-created_date')[:16])
                return render(request,
                              'search/product/search_product.html',
                              {'latest_product_list': latest_products, 'keyword_form': keyword_form,
                               'option_form': option_form, 'is_searched': True})

    keyword_form = SearchProductKeywordForm()
    option_form = SearchProductOptionForm()
    return render(request, 'search/product/search_product.html', {'keyword_form': keyword_form,
                                                                  'option_form': option_form, 'is_searched': False})


def search(request):
    query_keyword_string, is_sold_flags, price_range_pair, sort_method = parse_search_request(request)
    if not query_keyword_string:
        return []
    else:
        query_words = re.split(r"[\s]", query_keyword_string.rstrip())
        search_results = []
        if query_words is None:
            query_words = []
        for word in query_words:
            records_per_word = []
            for is_sold_flag in is_sold_flags:
                records_per_word += Product.objects.filter(title__icontains=word, price__gte=price_range_pair[0],
                                                           price__lt=price_range_pair[1], is_sold=is_sold_flag)
            for record in records_per_word:
                if record not in search_results:
                    search_results.append(record)
            search_results = sort_product_records_by(search_results, sort_method)
        return search_results


def search_product_ajax(request):
    if request.method == "GET":
        q = request.GET.get('q')
        search_results = get_public_product_list(search_ajax(q))
        if len(search_results) > 5:
            search_results = search_results[:5]
        minimal_search_results = [{'title': result.title} for result in search_results]
        if len(minimal_search_results) > 0:
            return JsonResponse(minimal_search_results, safe=False)
        else:
            return JsonResponse({'status': 'false'}, status=500)


def search_ajax(q):
        query_words = re.split(r"[\s]", q.rstrip())
        search_results = []
        if query_words is None:
            query_words = []
        for word in query_words:
            records_per_word = []
            records_per_word += Product.objects.filter(title__icontains=word)
            for record in records_per_word:
                if record not in search_results:
                    search_results.append(record)
        return search_results


def parse_search_request(request):
    query_keyword_string = request.GET.get("q")
    is_sold = request.GET.get("is_sold")
    if is_sold == 'all':
        is_sold_flags = (True, False)
    elif is_sold == 'sold_out':
        is_sold_flags = (True,)
    elif is_sold == 'not_sold': 
        is_sold_flags = (False,)
    if request.GET.get("price_range"):
        price_range_pair = [float(x) for x in request.GET.get("price_range").split('_')]
    else:
        price_range_pair = None
    sort_method = request.GET.get("sort_method")
    return (query_keyword_string, is_sold_flags, price_range_pair, sort_method)


def sort_product_records_by(product_records, sort_method):
    if sort_method == 'sort_new':
        return sorted(product_records, key=lambda instance: instance.created_date, reverse=True)
    elif sort_method == 'sort_old': 
        return sorted(product_records, key=lambda instance: instance.created_date)
    elif sort_method == 'sort_low': 
        return sorted(product_records, key=lambda instance: instance.price)
    elif sort_method == 'sort_high': 
        return sorted(product_records, key=lambda instance: instance.price, reverse=True)
    return []
