from django.db import migrations


class Migration(migrations.Migration):
    """
    Los campos avatar_url, bio y favorite_book nunca fueron añadidos
    al modelo Review en migraciones anteriores (solo existían en User),
    por lo que no hay nada que eliminar de la base de datos.
    Esta migración existe solo para mantener la cadena de dependencias.
    """

    dependencies = [
        ('core', '0006_book_pdf_url'),
    ]

    operations = []