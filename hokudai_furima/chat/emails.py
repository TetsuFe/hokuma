from django.conf import settings
from django.urls import reverse
from ..core.utils import build_absolute_uri, make_email_body_with_template
from django.core.mail import send_mail


def send_accept_new_message_email(product_pk, wanting_user_pk, message_send_user_name, to_email_address):
    chat_url = build_absolute_uri(
        reverse(
            'product:product_direct_chat',
            kwargs={'product_pk': product_pk, 'wanting_user_pk': wanting_user_pk}))
    send_mail('新規メッセージを受信しました（ホクマ）',
        make_email_body_with_template(message_send_user_name+"さんからメッセージを受信しました。\n" + chat_url),
        settings.DEFAULT_FROM_EMAIL,
        [to_email_address], fail_silently=False)
