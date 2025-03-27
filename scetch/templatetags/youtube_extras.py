from django import template
import re

register = template.Library()


@register.filter
def youtube_id(url):
    """
    Извлекает ID видео YouTube из различных форматов ссылок
    """
    if not url:
        return None

    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^#&?]{11})',  # Короткие ссылки
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com.*(?:\?v=|\&v=)([^#&?]{11})',  # Стандартные
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^#&?]{11})',  # Embed
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([^#&?]{11})',  # Устаревший
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?.*v=([^#&?]{11})'  # С параметрами
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match and match.group(1):
            return match.group(1)
    return None