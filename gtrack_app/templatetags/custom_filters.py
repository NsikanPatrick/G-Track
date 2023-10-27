# from django import template
# from django.db.models.query import QuerySet  # Import QuerySet
# from decimal import Decimal

# register = template.Library()

# @register.filter
# def sum_values(iterable):
#     if isinstance(iterable, list) or isinstance(iterable, QuerySet):
#         return sum(item.amount_owed for item in iterable)
#     return iterable

from django import template

register = template.Library()

@register.filter
def sum_values(amount_owed, iterable):
    total = sum(debtor.amount_owed for debtor in iterable)
    return '{:,.2f}'.format(total)
