# Generated by Django 4.2 on 2024-09-19 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_jobapplication"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="company_email",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
