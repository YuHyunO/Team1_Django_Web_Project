# Generated by Django 4.1 on 2022-08-09 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room_escape", "0002_alter_board_rdate_alter_board_udate_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="hit",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
