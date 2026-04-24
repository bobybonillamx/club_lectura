from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_book_reading_month_event_cover_font_social_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('is_default', models.BooleanField(default=False, help_text='Categoria predefinida del sistema')),
                ('order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(
                'core.Category',
                on_delete=models.SET_NULL,
                null=True, blank=True,
                related_name='books',
            ),
        ),
    ]