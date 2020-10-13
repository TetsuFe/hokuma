from django.test import TestCase, Client
from django.urls import reverse
from hokudai_furima.account.models import User


def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
    return user


def comfirm_site_rules(user):
    user.is_rules_confirmed = True
    user.save()
    return user


def activate_user(user):
    user.is_active = True
    user.save()
    return user


class MypageViewTests(TestCase):
    def test_not_login_mypage_status_code_302(self):
        client = Client()
        response = client.get(reverse('account:mypage'))
        self.assertEqual(
            response.status_code,
            302
        )

    def test_loggedin_mypage_status_code_200(self):
        user = create_user('test1', 'test1@eis.hokudai.ac.jp', 'hokuma1')
        user.set_password(user.password)
        user = activate_user(user)
        user = comfirm_site_rules(user)
        client = Client()
        # client.force_login(user, backend='django.contrib.auth.backends.ModelBackend')
        client.login(username='test1', password='hokuma1')
        response = client.get(reverse('account:mypage'))
        self.assertEqual(
            response.status_code,
            200
        )
