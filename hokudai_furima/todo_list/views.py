from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from hokudai_furima.product.models import Product
from django.contrib import messages
from django.conf import settings
from .models import ReportToRecieveTodo, RatingTodo
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .utils import get_undone_todo_list, get_done_todo_list
from hokudai_furima.core.decorators import site_rules_confirm_required


def add_todo_list(request, message, relative_url):
    #relative_url = reverse('product:product_details', kwargs={'pk': product.pk})
    todo = Todo(user=request.user, message=message, relative_url=relative_url)
    todo.save()


@site_rules_confirm_required
@login_required
def show_todo_list(request):
    sorted_undone_todo_list = get_undone_todo_list(request.user)
    sorted_done_todo_list = get_done_todo_list(request.user)
    return render(request, 'todo_list/todo_list.html', {'undone_todo_list': sorted_undone_todo_list, 'done_todo_list': sorted_done_todo_list})


@site_rules_confirm_required
@login_required
def get_undone_number_ajax(request):
    undone_todo_number = len(get_undone_todo_list(request.user))
    return JsonResponse({'undone_todo_number': undone_todo_number})
