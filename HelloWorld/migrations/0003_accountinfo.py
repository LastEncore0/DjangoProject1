# Generated by Django 5.1.4 on 2025-01-07 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HelloWorld', '0002_booktypeinfo_bookinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=20)),
                ('account', models.FloatField()),
            ],
        ),
    ]