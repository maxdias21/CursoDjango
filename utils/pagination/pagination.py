from math import ceil
from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    # Pegar página do meio
    middle_page = ceil(qty_pages / 2)

    # Pegar range inicial
    start_range = current_page - middle_page

    # Pegar range final
    stop_range = current_page + middle_page

    # Tamanho da paginação
    total_pages = len(page_range)

    # Se o "start_range" for 0, vou adicionar o valor dela na variável "start_range_offset"
    # abs para transformar número negativo em positivo
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range_offset > 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range > total_pages:
        start_range = start_range - abs(stop_range - total_pages)

    pagination = page_range[start_range: stop_range]

    return {
        'pagination': pagination,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'current_page': current_page,
        'middle_range': middle_page,
        'start_range_out_of_range': current_page > middle_page,
        'last_range_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, querylist, per_page, qty_pages=4):
    try:
        # Pegar "page" no template "search"
        current_page = int(request.GET.get('page', 1))
    except:
        current_page = 1

    # Passar a queryset + quantidade de itens por página
    paginator = Paginator(querylist, per_page)

    # Pegar uma página
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(paginator.page_range, qty_pages, current_page)

    return page_obj, pagination_range
