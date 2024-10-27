# Generated by Django 5.1.1 on 2024-10-26 20:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studyapp", "0002_alter_stopwatch_id_studystreak"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="stopwatch",
            name="user",
            field=models.ForeignKey(
                default='1',
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="StudyStreak",
        ),
    ]