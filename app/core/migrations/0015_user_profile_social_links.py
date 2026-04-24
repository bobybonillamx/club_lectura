from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_default_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=120, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='website',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.CreateModel(
            name='UserSocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('network', models.CharField(max_length=80)),
                ('url', models.URLField()),
                ('icon', models.CharField(max_length=30, blank=True, default='link')),
                ('user', models.ForeignKey(
                    to='core.User',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='social_links',
                )),
            ],
        ),
    ]
