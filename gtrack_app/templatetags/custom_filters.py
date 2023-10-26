from decimal import Decimal
from django import template

register = template.Library()

@register.filter
def sum_values(iterable):
    if all(isinstance(value, Decimal) for value in iterable):
        return sum(iterable)
    else:
        return 0  # Default value if the items are not Decimals


