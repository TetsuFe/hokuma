from .models import ReportToRecieveTodo, RatingTodo

def get_undone_todo_list(user):
    undone_todo_list = list(ReportToRecieveTodo.objects.filter(user=user, is_done=False))
    undone_todo_list += list(RatingTodo.objects.filter(user=user, is_done=False))
    sorted_undone_todo_list = sorted(undone_todo_list, key=lambda instance: instance.created_date, reverse=True)
    return sorted_undone_todo_list

def get_done_todo_list(user):
    done_todo_list = list(ReportToRecieveTodo.objects.filter(user=user, is_done=True))
    done_todo_list += list(RatingTodo.objects.filter(user=user, is_done=True))
    sorted_done_todo_list = sorted(done_todo_list, key=lambda instance: instance.created_date, reverse=True)
    return sorted_done_todo_list
