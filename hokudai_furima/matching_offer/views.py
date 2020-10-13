from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MatchingOffer, MatchingOfferTalk
from hokudai_furima.core.decorators import site_rules_confirm_required
from .forms import MatchingOfferForm, MatchingOfferImageForm, MatchingOfferTalkForm
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils import html
from hokudai_furima.notification.models import Notification
from django.urls import reverse
from hokudai_furima.core.utils import is_object_form_and_imageforms_valid
from django.contrib import messages


def make_matching_offer_image_forms(request):
    matching_offer_image_forms = []
    for i, _file in enumerate(request.FILES.getlist('image')):
        matching_offer_image_forms.append(MatchingOfferImageForm(i, request.POST, {'image':_file}))
    return matching_offer_image_forms


def matching_offer_details(request, pk):
    matching_offer = get_object_or_404(MatchingOffer, pk=pk)
    talks = MatchingOfferTalk.objects.filter(matching_offer=matching_offer).order_by('created_date')
    talk_form = MatchingOfferTalkForm()
    return render(request, 'matching_offer/matching_offer_details.html', {'matching_offer': matching_offer, 'talks': talks, 'form': talk_form})


@site_rules_confirm_required
@login_required
def create_matching_offer(request):
    if request.method == "POST":
        matching_offer_image_forms = []
        for i, _file in enumerate(request.FILES.getlist('image')):
            matching_offer_image_forms.append(MatchingOfferImageForm(i, request.POST, {'image':_file}))
        matching_offer_form = MatchingOfferForm(request.POST)
        if is_object_form_and_imageforms_valid(matching_offer_form, matching_offer_image_forms):
            matching_offer = matching_offer_form.save(commit=False)
            matching_offer.host = request.user
            matching_offer.save()
            for matching_offer_image_form in matching_offer_image_forms:
                matching_offer_image = matching_offer_image_form.save(commit=False)
                matching_offer_image.matching_offer = matching_offer
                matching_offer_image.save()
                matching_offer.matchingofferimage_set.add(matching_offer_image)
            matching_offer.save()
            messages.success(request, '募集の投稿に成功しました')
            return redirect('matching_offer:matching_offer_details', pk=matching_offer.pk)
    else:
        matching_offer_form = MatchingOfferForm()
    matching_offer_image_forms = [MatchingOfferImageForm(_i) for _i in range(4)]
    return render(request, 'matching_offer/create_matching_offer.html', {'matching_offer_form': matching_offer_form, 'matching_offer_image_forms': matching_offer_image_forms})


@site_rules_confirm_required
@login_required
def update_matching_offer(request, matching_offer_pk):
    matching_offer = get_object_or_404(MatchingOffer, pk=matching_offer_pk)
    matching_offer_seller_id = matching_offer.host.id
    if matching_offer_seller_id != request.user.id:
        return HttpResponse('invalid request')
    else:
        if request.method == "POST":
            matching_offer_form = MatchingOfferForm(request.POST, instance=matching_offer)
            matching_offer_image_forms = make_matching_offer_image_forms(request)
            if is_object_form_and_imageforms_valid(matching_offer_form, matching_offer_image_forms):
                matching_offer = matching_offer_form.save(commit=False)
                matching_offer.save()
                changed_image_flags = [request.POST['image_'+str(i)+'_exists'] for i in range(4)]
                before_matching_offer_images = [bpi for bpi in matching_offer.matchingofferimage_set.all()]
                posted_images = request.FILES.getlist('image')
                posted_image_index = 0
                for image_form_index, flag in enumerate(changed_image_flags):
                    if flag == '1':
                        if posted_image_index < len(posted_images):
                            if image_form_index < len(before_matching_offer_images):
                                matching_offer_image = before_matching_offer_images[image_form_index]
                                matching_offer_image.image = matching_offer_image_forms[posted_image_index].save(commit=False).image
                                matching_offer_image.matching_offer = matching_offer
                                matching_offer_image.update()
                                posted_image_index += 1
                            else:
                                matching_offer_image = matching_offer_image_forms[posted_image_index].save(commit=False)
                                matching_offer_image.matching_offer = matching_offer
                                matching_offer_image.save()
                                matching_offer.matchingofferimage_set.add(matching_offer_image)
                                matching_offer.save()
                                posted_image_index += 1
                    elif flag == '2':
                        before_matching_offer_image = before_matching_offer_images[image_form_index]
                        before_matching_offer_image.delete()
                messages.success(request, '募集情報を更新しました')
                return redirect('matching_offer:matching_offer_details', pk=matching_offer.pk)

        matching_offer_form = MatchingOfferForm(instance=matching_offer)
        matching_offer_image_forms = []
        matching_offer_images = matching_offer.matchingofferimage_set.all()
        matching_offer_image_thumbnail_urls = [matching_offer_image.thumbnail_url for matching_offer_image in matching_offer_images]
        for _i in range(4):
            if _i < len(matching_offer_images):
                matching_offer_image_forms.append(MatchingOfferImageForm(_i, instance=matching_offer_images[_i]))
            else:
                matching_offer_image_forms.append(MatchingOfferImageForm(_i))
        return render(request, 'matching_offer/update_matching_offer.html', {'matching_offer_form': matching_offer_form, 'matching_offer_image_forms': matching_offer_image_forms, 'matching_offer':matching_offer, 'matching_offer_image_thumbnail_urls': matching_offer_image_thumbnail_urls, 'placeholder_image_number_list': range(len(matching_offer_image_thumbnail_urls), 4)})


def show_latest_matching_offer_list(request):
    MAX_NUM_LATEST_MATCHING_OFFER = 80
    latest_matching_offer_list = MatchingOffer.objects.all().order_by('-created_date')[:MAX_NUM_LATEST_MATCHING_OFFER]
    return render(request, 'matching_offer/latest_matching_offer_list.html', {'matching_offer_list': latest_matching_offer_list})


@site_rules_confirm_required
@login_required
def create_offer_talk(request):
    talker = request.user
    text = request.POST.get('text')
    matching_offer_id = request.POST.get('matching_offer_id')
    matching_offer = MatchingOffer.objects.get(id=matching_offer_id)
    created_date = timezone.now()
    talk = MatchingOfferTalk(talker=talker, matching_offer=matching_offer, text=text, created_date=created_date)
    talk.save()

    """ メール・お知らせ通知（一回でもDMにメッセージを送った人or作成者に送る）
    relative_url = reverse('matching_offer:details', kwargs={'pk': matching_offer.pk})
    joined_chat_users = matching_offer.talk_set.all().distinct('talker')
    if matching_offer.host not in joined_chat_users:
        joined_chat_users.append(matching_offer.host)
        for joined_chat_user in joined_chat_users:
            if joined_chat_user != requeset.user:
                talk_reciever = joined_chat_user
                notice = Notification(reciever=talk_reciever, message=request.user.username+'から'+matching_offer.title+'についてのDMが届いています。', relative_url=relative_url)
                notice.save()
                send_email_accept_new_message_of_matching_offer(talk_reciever.email, matching_offer, request.user.username)
    """

    d = {
        'talker': html.escape(talker.username),
        'text': html.escape(text),
        'created_date': timezone.template_localtime(created_date, settings.TIME_ZONE).strftime('%Y年%-m月%-d日%-H:%M'),
        'talk_id': talk.id,
    }
    return JsonResponse(d)


@site_rules_confirm_required
@login_required
def delete_offer_talk(request):
    talk_id = request.POST.get('talk_id')
    talk = MatchingOfferTalk.objects.get(id=talk_id)
    if request.user == talk.talker:
        talk.delete()
        d = {
            'talk_id': talk_id
        }
        return JsonResponse(d)
    else:
        return JsonResponse({'status':'false'}, status=500)
