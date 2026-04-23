from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_user_suspension_notifications_seo'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='reading_month',
            field=models.CharField(
                max_length=7, blank=True, default='',
                help_text='Mes planeado de lectura. Formato YYYY-MM. Solo aplica para libros Por leer.',
            ),
        ),
        migrations.AddField(
            model_name='event',
            name='cover_image_url',
            field=models.URLField(blank=True, default='', help_text='Imagen de portada del evento.'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='custom_font_url',
            field=models.CharField(
                max_length=500, blank=True, default='',
                help_text='URL de Google Fonts. Ej: https://fonts.googleapis.com/css2?family=Merriweather',
            ),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='custom_font_serif',
            field=models.CharField(max_length=120, blank=True, default='', help_text='Nombre de la fuente para titulos. Ej: Merriweather'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='custom_font_sans',
            field=models.CharField(max_length=120, blank=True, default='', help_text='Nombre de la fuente para texto. Ej: Nunito'),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='icon',
            field=models.CharField(
                max_length=30, blank=True, default='link',
                choices=[
                    ('link', 'Enlace generico'),
                    ('instagram', 'Instagram'),
                    ('facebook', 'Facebook'),
                    ('twitter', 'Twitter / X'),
                    ('whatsapp', 'WhatsApp'),
                    ('telegram', 'Telegram'),
                    ('youtube', 'YouTube'),
                    ('tiktok', 'TikTok'),
                    ('spotify', 'Spotify'),
                    ('email', 'Correo electronico'),
                    ('website', 'Sitio web'),
                ],
            ),
        ),
    ]