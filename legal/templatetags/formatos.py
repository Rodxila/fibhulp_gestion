from django import template

register = template.Library()

@register.filter
def formato_europeo(valor):
    try:
        valor = float(valor)
        return "{:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return valor
