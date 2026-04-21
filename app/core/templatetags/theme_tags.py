from django import template
from core.models import THEMES

register = template.Library()

@register.filter
def theme_page_color(theme_key):
    return THEMES.get(theme_key, THEMES['literario_cafe'])['page']

@register.filter
def theme_primary_color(theme_key):
    return THEMES.get(theme_key, THEMES['literario_cafe'])['primary']

@register.filter
def theme_ink_color(theme_key):
    return THEMES.get(theme_key, THEMES['literario_cafe'])['ink']