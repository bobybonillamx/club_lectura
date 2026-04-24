from django.db import migrations

DEFAULT_CATEGORIES = [
    'Novela', 'Cuento', 'Poesia', 'Ensayo', 'Biografia',
    'Historia', 'Ciencia ficcion', 'Terror', 'Romance',
    'Autoayuda', 'Filosofia', 'Negocios', 'Infantil', 'Comics',
]


def add_default_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    for i, name in enumerate(DEFAULT_CATEGORIES):
        Category.objects.get_or_create(name=name, defaults={'is_default': True, 'order': i})


def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    Category.objects.filter(is_default=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_book_categories'),
    ]

    operations = [
        migrations.RunPython(add_default_categories, remove_default_categories),
    ]