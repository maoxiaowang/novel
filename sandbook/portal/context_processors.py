from portal.forms.account import AuthenticationForm


def portal_common(request):
    context = dict()
    # if request.user.is_authenticated:
    #     ...
    context.update(login_form=AuthenticationForm(auto_id=False))

    return context
