# Generated by Django 4.2 on 2023-04-06 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_useraccount_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='account_type',
            field=models.CharField(max_length=50),
        ),
    ]
