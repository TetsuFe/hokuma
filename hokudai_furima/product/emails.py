from django.conf import settings
from django.urls import reverse
from ..core.utils import build_absolute_uri, make_email_body_with_template
from django.core.mail import send_mail
from hokudai_furima.account.models import User
from .models import Product


def send_want_your_product_email(product_pk, wanting_user_pk, to_email_address):
    product_url = build_absolute_uri(
        reverse(
            'product:product_details',
            kwargs={'pk': product_pk}))
    wanting_user = User.objects.get(pk=wanting_user_pk)
    product = Product.objects.get(pk=product_pk)
    send_mail('商品の購入希望のお知らせ（ホクマ）',
          make_email_body_with_template(wanting_user.username+'さんが「'+product.title+"」の購入を希望しました。\n" + product_url),
          settings.DEFAULT_FROM_EMAIL,
          [to_email_address], fail_silently=False)

def send_rating_other_email(product_pk, rated_user_name, to_email_address):
    rating_url = build_absolute_uri(
        reverse(
            'rating:post_rating',
            kwargs={'product_pk': product_pk}))
    product = Product.objects.get(pk=product_pk)
    send_mail('取引相手の評価のお願い（ホクマ）',
          make_email_body_with_template(rated_user_name+'さんとの間での「'+product.title+'」の受け渡しの完了を確認しました。最後に取引相手を評価してください。\n'+rating_url),
          settings.DEFAULT_FROM_EMAIL,
          [to_email_address], fail_silently=False)

def send_decided_buyer_email(product_pk, wanting_user_pk, to_email_address):
    chat_url = build_absolute_uri(
        reverse(
            'product:product_direct_chat',
            kwargs={'product_pk': product_pk, 'wanting_user_pk': wanting_user_pk}))
    product = Product.objects.get(pk=product_pk)
    send_mail('購入希望中の商品について（ホクマ）',
          make_email_body_with_template(product.seller.username+'さんが「'+product.title+'」をあなたに販売することを確定しました。チャットで出品者と取引方法を確認し合ってください\n'+chat_url),
          settings.DEFAULT_FROM_EMAIL,
          [to_email_address], fail_silently=False)

def send_cancel_your_product_email(product_pk, wanting_user_pk, to_email_address):
    product_url = build_absolute_uri(
        reverse(
            'product:product_details',
            kwargs={'pk': product_pk}))
    wanting_user = User.objects.get(pk=wanting_user_pk)
    product = Product.objects.get(pk=product_pk)
    send_mail('商品の購入希望キャンセルのお知らせ（ホクマ）',
          make_email_body_with_template(wanting_user.username+'さんが「'+product.title+"」の購入希望をキャンセルしました。悪質なキャンセル行為と感じた場合は、ホクマ運営のお問い合わせメールアドレス（support@example.com）までご報告ください。\n" + product_url),
          settings.DEFAULT_FROM_EMAIL,
          [to_email_address], fail_silently=False)
