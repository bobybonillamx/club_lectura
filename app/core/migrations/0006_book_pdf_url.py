from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_user_profile_and_book_voting_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pdf_url',
            field=models.URLField(blank=True),
        ),
    ]
