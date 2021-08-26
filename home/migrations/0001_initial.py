# Generated by Django 3.2.6 on 2021-08-26 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AccountHolderId', models.CharField(max_length=50)),
                ('AccountId', models.CharField(max_length=50)),
                ('salutation', models.CharField(max_length=5)),
                ('firstName', models.CharField(max_length=100)),
                ('middleName', models.CharField(max_length=100, null=True)),
                ('lastName', models.CharField(max_length=100)),
                ('Gender', models.CharField(max_length=10)),
                ('Aadhar', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
