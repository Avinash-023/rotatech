# Generated by Django 5.1.4 on 2025-02-03 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0006_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
