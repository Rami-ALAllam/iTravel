# Generated by Django 2.2.4 on 2024-01-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_bill_expiration'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='country',
            field=models.CharField(default='USA', max_length=45),
        ),
        migrations.AddField(
            model_name='feedback',
            name='img',
            field=models.CharField(default='https://img.freepik.com/premium-vector/user-profile-icon-flat-style-member-avatar-vector-illustration-isolated-background-human-permission-sign-business-concept_157943-15752.jpg', max_length=225),
        ),
    ]
