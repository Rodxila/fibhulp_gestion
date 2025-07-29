from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    try:
        return d.get(key, {})
    except AttributeError:
        return {}

@register.filter
def zip_lists(a, b):
    try:
        return zip(a, b)
    except TypeError:
        return []

@register.filter
def formato_europeo(valor):
    try:
        valor = float(valor)
        return "{:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return valor

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return None

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except Exception:
        return None
