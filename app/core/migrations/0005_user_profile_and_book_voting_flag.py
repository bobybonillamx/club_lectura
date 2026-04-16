from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_clubsettings_google_credentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_book',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='book',
            name='allow_voting',
            field=models.BooleanField(default=True),
        ),
    ]
