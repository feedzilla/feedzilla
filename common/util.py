from django.template.defaultfilters import date
from django.core.paginator import Paginator, EmptyPage, InvalidPage

def format_date(date_obj, format=None):
    format = format if format else 'd F Y'
    return date(date_obj, format)


def paginate(qs, request, per_page=15):
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1

    paginator = Paginator(qs, per_page)
    try:
        page = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page_number = 1
        page = paginator.page(1)
    return page, paginator
