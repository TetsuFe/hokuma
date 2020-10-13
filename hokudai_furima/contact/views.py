# coding=utf-8
from .models import Contact
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def post_contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        contact = form.save()
        messages.success(request, "お問い合わせ内容を送信しました。お問い合わせに対する対応は、メールにてお知らせいたします。")
        return redirect('contact:post_success', pk=contact.pk)  # redirect('アプリケーション名:メソッド名')
    return render(request, 'contact/post_contact.html', {'form': form})


def post_success(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    email = contact.email
    text = contact.text
    return render(request, 'contact/post_success.html', {
        'email': email,
        'text': text,
    })
