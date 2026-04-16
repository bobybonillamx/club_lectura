from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_clubsettings_accent_review_moderation'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubsettings',
            name='google_login_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
