from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_clubsettings_theme_footer_seo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='meta_keywords',
            field=models.CharField(max_length=255, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='meta_author',
            field=models.CharField(max_length=120, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='notify_new_book',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='notify_new_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='notify_voting_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='notify_pending_approvals',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_tpl_new_book',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_tpl_new_event',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='email_tpl_voting_open',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='clubsettings',
            name='last_cron_run',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]