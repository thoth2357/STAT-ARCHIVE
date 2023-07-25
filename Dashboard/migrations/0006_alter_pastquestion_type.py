# Generated by Django 4.2.2 on 2023-07-21 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Dashboard", "0005_project_type_textbook_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pastquestion",
            name="Type",
            field=models.CharField(
                choices=[
                    ("Exam Questions", "Exam Questions"),
                    ("Test Questions", "Test Questions"),
                ],
                max_length=50,
            ),
        ),
    ]