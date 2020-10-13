# inspired: https://github.com/mirumee/saleor/blob/eb1deda79d1f36bc8ac5979fc58fc37a758c92c2/saleor/account/forms.py

from django import forms
from ..account.models import User
from django.contrib.auth import forms as django_forms, update_session_auth_hash
from . import emails
import re


class SignupForm(django_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email',)
        
    def clean(self):
        cleaned_data=super().clean()
        email = cleaned_data.get("email")
        m = re.search('hokudai.ac.jp$',email)
        if m is None:
            self._errors["email"]=["登録に使えるのはhokudai.ac.jpを持つメールアドレスのみです。"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text= "登録に使えるのはhokudai.ac.jpを持つメールアドレスのみです。"


class LoginForm(django_forms.AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].label = "メールアドレスまたはユーザ名"
        if request:
            email = request.GET.get('email')
            print(email)
            if email:
                self.fields['username'].initial = email

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        m = re.search('hokudai.ac.jp$', username_or_email)
        if m is not None:
            email = username_or_email
            try:
                user = User.objects.get(email=email)
                if user:
                    self.cleaned_data['username'] = user.username
            except:
                pass
        super().clean()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('icon','username','email','intro')
        #fields = ('username','email','intro')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['icon'].widget = forms.FileInput()
        self.fields['icon'].widget.attrs={'style':'display:none;', 'id':'icon' , 'onchange': 'fileget(this,\'0\');', }

class ChangePasswordForm(django_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].user = self.user
        self.fields['old_password'].widget.attrs['placeholder'] = ''
        self.fields['new_password1'].widget.attrs['placeholder'] = ''
        del self.fields['new_password2']

def logout_on_password_change(request, user):
    if (update_session_auth_hash is not None and
            not settings.LOGOUT_ON_PASSWORD_CHANGE):
        update_session_auth_hash(request, user)

class PasswordResetForm(django_forms.PasswordResetForm):
    """Allow resetting passwords.
    This subclass overrides sending emails to use templated email.
    """
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if email:
            users = User.objects.filter(email=email)
            if not users or not users[0].is_active:
                self._errors["email"]=["そのメールアドレスのアカウントは存在しないか本登録がされていません"]

    def get_users(self, email):
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        return active_users

    def send_mail(
            self, subject_template_name, email_template_name, context,
            from_email, to_email, html_email_template_name=None):
        # Passing the user object to the Celery task throws an
        # error "'User' is not JSON serializable". Since it's not used in our
        # template, we remove it from the context.
        del context['user']
        #emails.send_password_reset_email.delay(context, to_email)
        emails.send_password_reset_email(context, to_email)

class DeleteAccountForm(forms.Form):
    password = forms.CharField(label='パスワード', max_length=256, widget=forms.PasswordInput())
    def is_valid(self, user):
        if super().is_valid():
            if not user.check_password(self.cleaned_data['password']):
                self._errors["password"] = ["正しいパスワードを入力してください。"]
            else:
                return True
        return False
