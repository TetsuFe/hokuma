from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import datetime
from hokudai_furima.account.models import User
from hokudai_furima.product.models import Product
from hokudai_furima.chat.models import Chat, Talk


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


def create_product(user, title, description, price):
    product = Product.objects.create(seller=user, title=title, description=description, price=price)
    return product


def create_chat(product, product_wanting_user, product_seller):
    chat = Chat.objects.create(product=product,
                               product_wanting_user=product_wanting_user,
                               product_seller=product_seller,
                               created_date=timezone.now())
    return chat


def add_talk_to_chat(talker, chat, sentence, days):
    time = timezone.now() + datetime.timedelta(days=days)
    talk = Talk.objects.create(talker=talker, chat=chat, sentence=sentence, created_date=time)
    chat.talk_set.add(talk)


class ProductDirectChatViewTests(TestCase):
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        seller = create_user('test1', 'test1@eis.hokudai.ac.jp', 'hokuma1')
        wanting_user = create_user('test2', 'test2@eis.hokudai.ac.jp', 'hokuma2')
        seller = activate_user(seller)
        wanting_user = activate_user(wanting_user)
        seller = comfirm_site_rules(seller)
        wanting_user = comfirm_site_rules(wanting_user)
        product = create_product(seller, 'テスト商品', 'テスト商品です', 100)
        chat = create_chat(product, wanting_user, seller)
        add_talk_to_chat(talker=wanting_user, chat=chat, sentence='購入希望送らせていただきました', days=-2)
        add_talk_to_chat(talker=seller, chat=chat, sentence='購入希望ありがとうございます！', days=-1)
        client = Client()
        client.force_login(seller, backend='django.contrib.auth.backends.ModelBackend')
        response = client.get(reverse('product:product_direct_chat',
                                           kwargs={'product_pk': product.pk, 'wanting_user_pk': wanting_user.pk}))
        self.assertQuerysetEqual(
            response.context['talks'],
            ['<Talk: Talk object (1)>', '<Talk: Talk object (2)>']
        )


class ProductDetailsViewTests(TestCase):
    def test_product_details(self):
        seller = create_user('test1', 'test1@eis.hokudai.ac.jp', 'hokuma1')
        seller = activate_user(seller)
        seller = comfirm_site_rules(seller)
        product = create_product(seller, 'テスト商品', 'テスト商品です', 100)
        client = Client()
        response = client.get(reverse('product:product_details',
                                      kwargs={'pk': product.pk}))
        self.assertEqual(
            response.context['product'],
            product
        )
