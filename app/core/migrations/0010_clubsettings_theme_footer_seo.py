from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_clubsettings_smtp_domain_cover_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubsettings',
            name='theme',
            field=models.CharField(
                max_length=40,
                default='literario_cafe',
                choices=[
                    ('literario_cafe', 'Literario Cafe'),
                    ('moderno_oscuro', 'Moderno Oscuro'),
                    ('minimalista_blanco', 'Minimalista Blanco'),
                    ('verde_bosque', 'Verde Bosque'),
                    ('oceano_profundo', 'Oceano Profundo'),
                    ('rosa_editorial', 'Rosa Editorial'),
                    ('personalizado', 'Personalizado'),
                ],
            ),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='meta_description',
            field=models.CharField(max_length=260, blank=True, default='', help_text='Descripcion del sitio para buscadores (max 160 chars recomendado).'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='home_welcome_text',
            field=models.CharField(max_length=255, blank=True, default='', help_text='Texto de bienvenida en la pagina principal.'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='cta_register_text',
            field=models.CharField(max_length=60, blank=True, default='', help_text='Texto del boton de registro. Ej: Unete al club'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='cta_login_text',
            field=models.CharField(max_length=60, blank=True, default='', help_text='Texto del boton de login. Ej: Entrar'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='footer_powered_by_name',
            field=models.CharField(max_length=120, blank=True, default='', help_text='Nombre que aparece en Powered by. Dejar vacio para usar el predeterminado.'),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='footer_powered_by_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='footer_custom_link_text',
            field=models.CharField(max_length=120, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='footer_custom_link_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='footer_text',
            field=models.CharField(max_length=255, blank=True, default='', help_text='Texto libre adicional en el footer.'),
        ),
    ]