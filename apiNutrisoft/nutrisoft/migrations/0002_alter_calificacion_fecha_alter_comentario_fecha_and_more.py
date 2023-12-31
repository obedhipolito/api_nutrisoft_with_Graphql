# Generated by Django 4.2.5 on 2023-12-12 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrisoft', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='comentarios',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='likes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='url_imagen',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cedula',
            field=models.CharField(blank=True, max_length=22, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='informacion',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
