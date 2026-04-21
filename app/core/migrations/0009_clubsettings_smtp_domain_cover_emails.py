from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_clubsettings_icon_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubsettings',
            name='cover_image_url',
            field=models.URLField(blank=True, default='', help_text='Imagen de portada para la pagina principal.'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='public_domain',
            field=models.CharField(blank=True, default='', max_length=255, help_text='Dominio publico del sitio. Ej: miclub.com o club.midominio.com. Sin https://.'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='smtp_host',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='smtp_port',
            field=models.PositiveIntegerField(default=587),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='smtp_user',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='smtp_password',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='smtp_use_tls',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_from',
            field=models.CharField(blank=True, default='', max_length=255, help_text='Nombre y correo del remitente. Ej: Club de Lectura <club@midominio.com>'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_tpl_welcome',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_tpl_approved',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_tpl_invitation',
            field=models.TextField(blank=True, default=''),
        ),
    ]