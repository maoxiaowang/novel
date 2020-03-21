from base.constants.novel import BUILTIN_CATEGORIES


def common(request):
    context = dict()
    context['builtin_categories'] = BUILTIN_CATEGORIES
    context['ID'] = '00000000'
    return context
