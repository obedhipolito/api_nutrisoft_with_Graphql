# Generated by Django 4.2.5 on 2023-12-26 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrisoft', '0005_alter_publicacion_likes_alter_publicacion_url_imagen_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentario',
            options={'ordering': ['fecha']},
        ),
        migrations.RemoveField(
            model_name='publicacion',
            name='comentarios',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=20),
        ),
    ]