# Generated by Django 5.0 on 2023-12-29 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_todoworkerthrough_todolist_workers'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
