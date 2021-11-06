# Generated by Django 3.2.7 on 2021-11-06 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawfile',
            name='dpi',
            field=models.IntegerField(blank=True, default=None, verbose_name='DPI'),
        ),
        migrations.AlterField(
            model_name='processedfile',
            name='file_object',
            field=models.FileField(upload_to='output_files', verbose_name='File Object'),
        ),
        migrations.AlterField(
            model_name='rawfile',
            name='file_object',
            field=models.FileField(upload_to='input_files', verbose_name='File Object'),
        ),
    ]
