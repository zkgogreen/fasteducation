from django import template
import random

register = template.Library()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)

@register.filter(name='get_item')
def get_item(iterable, index):
    try:
        return iterable[index]
    except (IndexError, TypeError):
        return None