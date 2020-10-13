from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from .utils import fetch_notification_list
from django.http import JsonResponse
from hokudai_furima.core.decorators import site_rules_confirm_required


@site_rules_confirm_required
@login_required
def index(request):
    notification_list = fetch_notification_list(request)
    return render(request, 'notification/index.html', {'notification_list': notification_list})


@site_rules_confirm_required
@login_required
def get_unread_number_ajax(request):
    notification_number = len(Notification.objects.filter(reciever=request.user, unread=True))
    return JsonResponse({'notification_number': notification_number})
