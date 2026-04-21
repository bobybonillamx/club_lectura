from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_review_duplicate_user_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubsettings',
            name='icon_url',
            field=models.URLField(blank=True, default='', help_text='Icono cuadrado para PWA y favicon. Si logo_url esta vacio se usa este en la navbar.'),
        ),
    ]