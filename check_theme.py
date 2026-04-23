from core.models import ClubSettings
c = ClubSettings.get_solo()
print("tema:", c.theme)
print("primary_color:", c.primary_color)
print("accent_color:", c.accent_color)
print("custom_font_serif:", c.custom_font_serif)
print("custom_font_url:", c.custom_font_url[:60] if c.custom_font_url else "")