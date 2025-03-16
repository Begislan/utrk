from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Возвращает значение словаря по ключу."""
    return dictionary.get(key, [])

@register.filter
def split(value, delimiter=","):
    """Разделяет строку по указанному разделителю."""
    return value.split(delimiter)