from django.shortcuts import render
from .models import WatchList
from hokudai_furima.product.models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
#from .emails import send_accept_new_message_email
from hokudai_furima.core.decorators import site_rules_confirm_required


@site_rules_confirm_required
@login_required
def show_watch_list(request):
    try:
        watch_list = WatchList.objects.get(user=request.user)
        return render(request, 'watchlist/watchlist.html', {'watchlist_product_list': watch_list.product_set.all()})
    except WatchList.DoesNotExist:
        return render(request, 'watchlist/no_watchlist.html')


@site_rules_confirm_required
@login_required
def add_watch_list(request):
    try:
        watch_list = WatchList.objects.get(user=request.user)
    except WatchList.DoesNotExist:
        watch_list = WatchList(user=request.user)
        watch_list.save()
    product_pk = request.POST.get('product_pk')
    product = Product.objects.get(pk=product_pk)
    watch_list.product_set.add(product)
    watch_list.update()
    return JsonResponse({'success': True})


@site_rules_confirm_required
@login_required
def remove_from_watch_list(request):
    try:
        watch_list = WatchList.objects.get(user=request.user)
    except WatchList.DoesNotExist:
        watch_list = WatchList(user=request.user)
        watch_list.save()
    product_pk = request.POST.get('product_pk')
    product = Product.objects.get(pk=product_pk)
    watch_list.product_set.remove(product)
    watch_list.update()
    return JsonResponse({'success': True})


@site_rules_confirm_required
@login_required
def is_in_watch_list(request):
    try:
        watch_list = WatchList.objects.get(user=request.user)
        product_pk = request.GET.get('product_pk')
        if watch_list.product_set.filter(pk=product_pk).count() > 0:
            return JsonResponse({'is_in_watch_list': 'true'})
        else:
            return JsonResponse({'is_in_watch_list': 'false'})
    except WatchList.DoesNotExist:
        return JsonResponse({'is_in_watch_list': 'false'})
