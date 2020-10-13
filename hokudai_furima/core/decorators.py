from django.shortcuts import redirect

def site_rules_confirm_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_rules_confirmed:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('site_rules:confirm')
        else:
            return redirect('account:login')

    return _wrapped_view
