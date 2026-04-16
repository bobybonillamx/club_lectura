from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubsettings',
            name='accent_color',
            field=models.CharField(default='#212529', max_length=7),
        ),
        migrations.AddField(
            model_name='review',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='review',
            name='moderation_note',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
