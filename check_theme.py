from core.models import ClubSettings
c = ClubSettings.get_solo()
print("tema:", c.theme)
print("custom_font_serif:", c.custom_font_serif)
print("custom_font_sans:", c.custom_font_sans)
print("custom_font_url COMPLETA:")
print(c.custom_font_url)
tv = c.theme_vars
print("theme_vars fonts COMPLETA:")
print(tv.get('fonts'))
print("theme_vars serif:", tv.get('serif'))
print("theme_vars sans:", tv.get('sans'))
