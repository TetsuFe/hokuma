from django import template

register = template.Library()

@register.inclusion_tag('todo_list/_todo_list.html')
def show_todo_list(done_todo_list, undone_todo_list):
    return {'done_todo_list': done_todo_list, 'undone_todo_list': undone_todo_list}
