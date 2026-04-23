from core.models import ClubSettings
c = ClubSettings.get_solo()
print("tema en DB:", c.theme)
print("primary_color:", c.primary_color)
tv = c.theme_vars
print("theme_vars page:", tv.get('page'))
print("theme_vars primary:", tv.get('primary'))
print("theme_vars fonts:", tv.get('fonts', '')[:60])