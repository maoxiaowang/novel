from portal.forms.account import AuthenticationForm


def portal_common(request):
    context = dict()
    if request.user.is_authenticated:
        ...
    else:
        context.update(login_form=AuthenticationForm())

    return context
