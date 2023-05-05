# Generated by Django 4.1.5 on 2023-05-05 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_work"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tasks",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="main.project",
            ),
        ),
        migrations.AlterField(
            model_name="work",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="works",
                to="main.tasks",
            ),
        ),
    ]
