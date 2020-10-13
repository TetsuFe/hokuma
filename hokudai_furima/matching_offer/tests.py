from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import datetime
from hokudai_furima.account.models import User
from hokudai_furima.matching_offer.models import MatchingOffer, MatchingOfferTalk


def create_user(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password, is_active=True)
    return user


def confirm_site_rules(user):
    user.is_rules_confirmed = True
    user.save()
    return user


def activate_user(user):
    user.is_active = True
    user.save()
    return user


def create_matching_offer(user, title, description):
    product = MatchingOffer.objects.create(host=user, title=title, description=description)
    return product


def add_talk_to_matching_offer(talker, matching_offer, text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    MatchingOfferTalk.objects.create(talker=talker,
                                     matching_offer=matching_offer,
                                     text=text,
                                     created_date=time)


class ProductDirectChatViewTests(TestCase):
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        host = create_user('test1', 'test1@eis.hokudai.ac.jp', 'hokuma1')
        guest = create_user('test2', 'test2@eis.hokudai.ac.jp', 'hokuma2')
        host = activate_user(host)
        guest = activate_user(guest)
        host = confirm_site_rules(host)
        guest = confirm_site_rules(guest)
        matching_offer = create_matching_offer(host, 'テストオファー', 'テストオファーです')
        add_talk_to_matching_offer(guest, matching_offer, '行きたいです', days=-2)
        add_talk_to_matching_offer(host, matching_offer, 'ぜひ来てください！', days=-1)
        client = Client()
        client.force_login(host, backend='django.contrib.auth.backends.ModelBackend')
        response = client.get(reverse('matching_offer:matching_offer_details',
                                      kwargs={'pk': matching_offer.pk}))
        self.assertQuerysetEqual(
            response.context['talks'],
            ['<MatchingOfferTalk: MatchingOfferTalk object (1)>', '<MatchingOfferTalk: MatchingOfferTalk object (2)>']
        )
