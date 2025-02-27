# Generated by Django 5.1.4 on 2025-02-27 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0020_alter_courses_image_alter_courses_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('extracted_text', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
