# Generated by Django 5.1.4 on 2025-01-18 09:43

import django.db.models.query
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HelloWorld', '0004_alter_accountinfo_options_alter_accountinfo_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_folder', models.CharField(max_length=500, verbose_name='源文件夹')),
                ('target_folder', models.CharField(blank=True, max_length=500, verbose_name='目标文件夹')),
                ('output_format', models.CharField(choices=[('tga', 'TGA'), ('png', 'PNG'), ('jpg', 'JPG'), ('bmp', 'BMP'), ('gif', 'GIF'), ('tiff', 'TIFF')], default='tga', max_length=10, verbose_name='转换格式')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='bookName',
            field=models.CharField(max_length=20, verbose_name='書名'),
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='bookType',
            field=models.ForeignKey(on_delete=django.db.models.query.Prefetch, to='HelloWorld.booktypeinfo', verbose_name='類別'),
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='price',
            field=models.FloatField(verbose_name='價格'),
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='publishDate',
            field=models.DateField(verbose_name='出版日期'),
        ),
    ]
