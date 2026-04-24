from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, help_text='Orden de aparicion. 0 = automatico por fecha.'),
        ),
    ]
