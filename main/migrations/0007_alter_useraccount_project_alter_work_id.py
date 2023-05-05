# Generated by Django 4.1.5 on 2023-05-05 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_rename_file_work_files_alter_work_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="users",
                to="main.project",
            ),
        ),
        migrations.AlterField(
            model_name="work",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
