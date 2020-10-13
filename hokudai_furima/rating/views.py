from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import UserRatingForm
from .models import UserRating
from hokudai_furima.product.models import Product
from django.contrib import messages
from django.http import HttpResponse
from hokudai_furima.account.models import User
from hokudai_furima.notification.models import Notification
from django.contrib.auth.decorators import login_required
from hokudai_furima.todo_list.models import RatingTodo
from hokudai_furima.core.decorators import site_rules_confirm_required


@site_rules_confirm_required
@login_required
def post_rating(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if product.is_sold:
        if request.user == product.buyer:
            rated_user = product.seller
        elif request.user == product.seller:
            rated_user = product.buyer
        else:
            return HttpResponse('invalid request')
        if request.method == 'POST':
            rating = request.POST.get('rating')
            user_rating_form = UserRatingForm(request.POST)
            if not UserRating.objects.filter(product=product, rating_user=request.user):
                user_rating = UserRating(product=product, rating_user=request.user, rated_user=rated_user, rating=rating)
                user_rating.save()
                rating_todo = RatingTodo.objects.get(product=product, user=request.user)
                rating_todo.done()
                rating_todo.update()
                messages.success(request, 'ユーザ評価ありがとうございます。あなたの評価は相手のユーザページに反映されます。')
                response = redirect('account:others_page', user_pk=rated_user.pk)
                response['location'] += '?is_after_rating=true'
                return response
            else:
                messages.error(request, '評価は一度しかできません')

        user_rating_form = UserRatingForm()
        return render(request, 'rating/post_rating.html', {'form': user_rating_form, 'product_pk': product_pk, 'rated_user_name': rated_user.username})
    else:
        return HttpResponse('invalid request')
