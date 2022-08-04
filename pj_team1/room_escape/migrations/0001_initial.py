# Generated by Django 4.0.6 on 2022-08-04 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('pw', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('rdate', models.DateTimeField()),
                ('udate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room', models.TextField(primary_key=True, serialize=False)),
                ('loc', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=50)),
                ('theme_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('theme', models.TextField(primary_key=True, serialize=False)),
                ('img_path', models.TextField()),
                ('genre', models.CharField(max_length=255)),
                ('people', models.CharField(default='-', max_length=10)),
                ('info', models.TextField(default='-')),
                ('difficulty', models.CharField(default='0', max_length=10)),
                ('horror', models.CharField(default='0', max_length=10)),
                ('activity', models.CharField(default='0', max_length=10)),
                ('star', models.CharField(default='0', max_length=10)),
                ('recommend', models.IntegerField(default=0)),
                ('room', models.ForeignKey(db_column='room', on_delete=django.db.models.deletion.CASCADE, related_name='Theme_room', to='room_escape.room')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeReview',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.TextField()),
                ('rdate', models.DateTimeField()),
                ('udate', models.DateTimeField()),
                ('email', models.ForeignKey(db_column='email', on_delete=django.db.models.deletion.CASCADE, related_name='ThemeReview_email', to='room_escape.member')),
                ('theme', models.ForeignKey(db_column='theme', on_delete=django.db.models.deletion.CASCADE, related_name='ThemeReview_theme', to='room_escape.theme')),
            ],
        ),
        migrations.CreateModel(
            name='CafeReview',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('review', models.TextField()),
                ('rdate', models.DateTimeField()),
                ('udate', models.DateTimeField()),
                ('email', models.ForeignKey(db_column='email', on_delete=django.db.models.deletion.CASCADE, related_name='CafeReview_email', to='room_escape.member')),
                ('room', models.ForeignKey(db_column='room', on_delete=django.db.models.deletion.CASCADE, related_name='CafeReview_room', to='room_escape.room')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=20)),
                ('title', models.TextField(max_length=1000)),
                ('content', models.TextField()),
                ('rdate', models.DateTimeField()),
                ('udate', models.DateTimeField()),
                ('email', models.ForeignKey(db_column='email', on_delete=django.db.models.deletion.CASCADE, related_name='Board_email', to='room_escape.member')),
            ],
        ),
    ]