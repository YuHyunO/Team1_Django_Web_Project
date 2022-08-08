# Generated by Django 4.0.6 on 2022-08-08 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_escape', '0006_alter_room_img_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='rdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='udate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cafereview',
            name='rdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cafereview',
            name='udate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='pw',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='rdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='udate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='themereview',
            name='rdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='themereview',
            name='udate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]