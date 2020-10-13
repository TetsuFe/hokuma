from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def privacy_policy(request):
    return render(request, 'site_rules/privacy_policy.html')


def tos(request):
    return render(request, 'site_rules/tos.html')


@login_required
def confirm(request):
    return render(request, 'site_rules/confirm.html')


@login_required
def agree(request):
    user = request.user
    user.is_rules_confirmed = True
    user.save()
    messages.success(request, ('利用規約・プライバシーポリシーへの同意ありがとうございます。ホクマを使って楽しい大学ライフを！'))
    return redirect('home')
