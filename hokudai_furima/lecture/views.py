from django.shortcuts import render, get_object_or_404
from .models import LectureCategory
from hokudai_furima.product.utils import get_public_product_list


def count_all_node_children_related_product(_lecture_category_list):
    array = []
    for lecture_category in _lecture_category_list:
        all_children_leaf_product_count = \
            count_children_related_product(0, lecture_category)
        array.append({'content': lecture_category, 'leaf_product_count': all_children_leaf_product_count})
    return array


def count_children_related_product(count, node):
    if node.children.exists():
        for child_node in node.children.all():
            count += count_children_related_product(count, child_node)
        return count
    else:
        return node.lecture_category_products.count()


def lecture_category_list(request):
    _lecture_category_list = LectureCategory.objects.filter(level=0).order_by('id')
    lecture_category_dict_list = count_all_node_children_related_product(_lecture_category_list)
    return render(request, 'lecture/lecture_category_list.html',
                  {'lecture_category_dict_list': lecture_category_dict_list})


def lecture_category_list_with_pk(request, pk):
    lecture_category = get_object_or_404(LectureCategory, pk=pk)
    _lecture_category_list = lecture_category.children.all().order_by('id')
    lecture_category_dict_list = count_all_node_children_related_product(_lecture_category_list)
    return render(request, 'lecture/lecture_category_list.html',
                  {'lecture_category_dict_list': lecture_category_dict_list})


def lecture_category_details(request, pk):
    lecture_category = get_object_or_404(LectureCategory, pk=pk)
    lecture_category_parent_chain = [lecture_category]
    temp_parent_lecture_category = lecture_category.parent
    while temp_parent_lecture_category:
        lecture_category_parent_chain.append(temp_parent_lecture_category)
        temp_parent_lecture_category = temp_parent_lecture_category.parent
    lecture_category_parent_chain.reverse()
    lecture_category_products = get_public_product_list(lecture_category.lecture_category_products.all().order_by('-id'))

    child_lecture_categories = lecture_category.children.all().order_by('id')
    return render(request, 'lecture/lecture_category_details.html',
                  {'lecture_category': lecture_category, 'lecture_category_parent_chain': lecture_category_parent_chain,
                   'child_lecture_categories': child_lecture_categories,
                   'lecture_category_products': lecture_category_products})
