# Generated by Django 5.1.4 on 2025-01-18 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HelloWorld', '0005_imageconversion_alter_bookinfo_bookname_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageconversion',
            options={'verbose_name': 'convert_images'},
        ),
        migrations.AlterModelTable(
            name='imageconversion',
            table='t_convert_images',
        ),
    ]
