# Generated by Django 3.0.10 on 2020-10-07 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customermodel_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='category',
            field=models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'), ('Both', 'Both')], max_length=255, null=True),
        ),
    ]
