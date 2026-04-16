from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_clubsettings_google_login_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubsettings',
            name='google_client_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='google_client_secret',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
