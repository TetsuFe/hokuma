from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as auth_views # in login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from .forms import SignupForm, LoginForm, UserEditForm, ChangePasswordForm, PasswordResetForm, logout_on_password_change, DeleteAccountForm
from django.contrib.auth.decorators import login_required
import re
from .models import User
from hokudai_furima.rating.models import UserRating
from hokudai_furima.notification.models import Notification
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .emails import send_account_activation_email
from django.contrib.auth.tokens import default_token_generator
from hokudai_furima.product.models import Product
from copy import deepcopy
from hokudai_furima.product.utils import get_public_product_list
from hokudai_furima.todo_list.utils import get_undone_todo_list, get_done_todo_list
from hokudai_furima.notification.utils import fetch_notification_list
from hokudai_furima.core.decorators import site_rules_confirm_required
from hokudai_furima.matching_offer.models import MatchingOffer


# inspired: https://github.com/mirumee/saleor/blob/eb1deda79d1f36bc8ac5979fc58fc37a758c92c2/saleor/account/views.py
# How to log a user in https://docs.djangoproject.com/en/2.0/topics/auth/default/

def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = user.username
        email = user.email
        password = user.password
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password)
        #auth.authenticate は、is_activeをfalseにすると失敗する
        #user = auth.authenticate(request=request, username=username, password=password)
        # activateモデルの作成と保存。userモデルを紐づけています。
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)
        # メール本文の「本登録はこちら！ http://...」のURLを作成する
        #base_url = "/".join(request.build_absolute_uri().split("/")[:4])
        #base_url_without_port = re.sub(':\d+','',base_url) 
        #activation_url = "{0}/activation/{1}".format(base_url_without_port, activate_key)
 
        #send_activation_mail(user.email, activation_url)
        context = {'uid': uidb64, 'token': token}
        to_email_address = user.email
        send_account_activation_email(context, to_email_address)

        messages.success(request, ('仮登録が完了しました。ログインするためには、認証メールのリンクにアクセスする必要があります。'))
        redirect_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        return redirect(redirect_url)
    ctx = {'form': form}
    return render(request, 'account/signup.html', ctx)

def login(request, backends='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        redirect_url = request.POST.get('next', settings.LOGIN_REDIRECT_URL)
        return redirect(redirect_url)
    kwargs = {
        'template_name': 'account/login.html',
        'authentication_form': LoginForm}
    return auth_views.LoginView.as_view(**kwargs)(request, **kwargs)


@site_rules_confirm_required
@login_required
def mypage(request):
    wanting_product_list = get_public_product_list(Product.objects.filter(wanting_users=request.user).order_by('-id'))
    selling_product_list = Product.objects.filter(seller=request.user).order_by('-id')
    notification_list = fetch_notification_list(request)
    sorted_undone_todo_list = get_undone_todo_list(request.user)
    sorted_done_todo_list = get_done_todo_list(request.user)
    my_matching_offer_list = MatchingOffer.objects.filter(host=request.user).order_by('-id')
    return render(request, 'account/mypage.html', {'wanting_product_list': wanting_product_list, 'selling_product_list': selling_product_list, 'my_matching_offer_list': my_matching_offer_list, 'notification_list': notification_list, 'done_todo_list': sorted_done_todo_list, 'undone_todo_list': sorted_undone_todo_list})


def others_page(request, user_pk):
    others_user = get_object_or_404(User, pk=user_pk)
    good_rating_count = UserRating.objects.filter(rated_user=others_user, rating='good').count()
    normal_rating_count = UserRating.objects.filter(rated_user=others_user, rating='normal').count()
    bad_rating_count = UserRating.objects.filter(rated_user=others_user, rating='bad').count()
    others_user_product_list = get_public_product_list(Product.objects.filter(seller=others_user))
    contexts = {'others_user': others_user, 'good_rating_count': good_rating_count,
                'normal_rating_count': normal_rating_count, 'bad_rating_count': bad_rating_count,
                'others_user_product_list': others_user_product_list}
    is_after_rating_key = 'is_after_rating'
    is_after_rating_parameter = request.GET.get(is_after_rating_key)
    if is_after_rating_parameter:
        contexts[is_after_rating_key] = is_after_rating_parameter
    return render(request, 'account/others_page.html', contexts)


@login_required
def logout(request):
    auth.logout(request)
    #messages.success(request, ('ログアウトしました'))
    return redirect(settings.LOGIN_REDIRECT_URL)


def activation(request, uidb64, token):
    """ /activation/:アクティベーションキー でアクセス。本登録画面 """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, ('本登録が完了しました。北大フリマへようこそ！'))
        return redirect('account:mypage')
    else:
        return HttpResponse("Activation link has expired")

def password_reset(request):
    kwargs = {
        'template_name': 'account/password_reset.html',
        'success_url': reverse_lazy('account:reset-password-done'),
        'form_class': PasswordResetForm}
    return auth_views.PasswordResetView.as_view(**kwargs)(request, **kwargs)

class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_from_key.html'
    success_url = reverse_lazy('account:reset-password-complete')
    token = None
    uidb64 = None

def password_reset_confirm(request, uidb64=None, token=None):
    kwargs = {
        'template_name': 'account/password_reset_from_key.html',
        'success_url': reverse_lazy('account:reset-password-complete'),
        'token': token,
        'uidb64': uidb64}
    return PasswordResetConfirm.as_view(**kwargs)(request, **kwargs)


def get_or_process_password_form(request):
    form = ChangePasswordForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        logout_on_password_change(request, form.user)
        messages.success(request, pgettext(
            'Storefront message', 'Password successfully changed.'))
    return form


@site_rules_confirm_required
@login_required
def edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('プロフィール情報を変更しました。'))
        else:
            for _field in form:
                for error in _field.errors:
                    messages.error(request, error,extra_tags=('danger'))
            return render(request, 'account/mypage.html', {'form': form, 'product_list': wanting_product_list})
    form = UserEditForm(instance=request.user)
    return render(request, 'account/edit.html', {'form': form})


@site_rules_confirm_required
@login_required
def delete(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        user = User.objects.get(email=request.user.email)
        if form.is_valid(user):
            user.is_active = False
            user.save()
            messages.success(request, '退会処理が完了しました。')
            return redirect('account:login')
    else:
        form = DeleteAccountForm()
    return render(request, 'account/delete_account.html', {'form': form})
