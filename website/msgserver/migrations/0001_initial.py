# Generated by Django 3.2.9 on 2021-11-17 22:05

from django.db import migrations, models
import msgserver.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('key', models.CharField(max_length=8, primary_key=True, serialize=False, validators=[msgserver.models.validate_key])),
                ('msg', models.CharField(max_length=160)),
            ],
        ),
    ]
