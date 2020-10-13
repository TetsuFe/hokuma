#from celery import shared_task
from django.conf import settings
from django.urls import reverse
#from templated_email import send_templated_mail
from ..core.utils import build_absolute_uri, make_email_body_with_template
from django.core.mail import send_mail


#@shared_task
def send_password_reset_email(context, to_email_address):
    reset_url = build_absolute_uri(
        reverse(
            'account:reset-password-confirm',
            kwargs={'uidb64': context['uid'], 'token': context['token']}))
    
    send_mail('パスワード再設定メール（ホクマ）',
        make_email_body_with_template("パスワードの再設定をご希望の場合は、以下のURLにアクセスしてください。\n" + reset_url),
        settings.DEFAULT_FROM_EMAIL,
        [to_email_address], fail_silently=False)

def send_account_activation_email(context, to_email_address):
    activation_url = build_absolute_uri(
        reverse(
            'account:activation',
            kwargs={'uidb64': context['uid'], 'token': context['token']}))
    send_mail('仮登録完了のお知らせ（ホクマ）',
        make_email_body_with_template("「北大フリマ」にご登録いただきありがとうございます。以下のURLにアクセスすることで本登録完了となり、ログインが可能になります。\n" + activation_url),
        settings.DEFAULT_FROM_EMAIL,
        [to_email_address], fail_silently=False)
