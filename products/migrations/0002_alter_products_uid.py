# Generated by Django 4.1.3 on 2022-12-16 16:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='uid',
            field=models.UUIDField(default=uuid.UUID('e24f627d-fbcd-4822-9f90-32646e13f048'), primary_key=True, serialize=False),
        ),
    ]
