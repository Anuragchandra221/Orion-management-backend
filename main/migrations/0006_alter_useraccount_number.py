# Generated by Django 4.2 on 2023-04-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_useraccount_register'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
