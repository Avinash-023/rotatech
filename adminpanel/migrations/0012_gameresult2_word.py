# Generated by Django 5.1.4 on 2025-02-10 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0011_gameresult2'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult2',
            name='word',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
