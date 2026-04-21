from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_book_pdf_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='avatar_url',
        ),
        migrations.RemoveField(
            model_name='review',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='review',
            name='favorite_book',
        ),
    ] 